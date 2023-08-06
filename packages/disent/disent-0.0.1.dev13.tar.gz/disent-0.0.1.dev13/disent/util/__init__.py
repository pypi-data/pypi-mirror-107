#  ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  MIT License
#
#  Copyright (c) 2021 Nathan Juraj Michlo
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#  ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~

import functools
import logging
import os
import time
from collections import Sequence
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from itertools import islice
from pprint import pformat
from typing import List

import numpy as np
import pytorch_lightning as pl
import torch


"""
helpful functions that do not fit nicely into any other file.
"""

log = logging.getLogger(__name__)

# ========================================================================= #
# seeds                                                                     #
# ========================================================================= #


def is_test_run():
    """
    This is used internally to test some scripts. There is no need
    to use this function in your own scripts.
    """
    return bool(os.environ.get('DISENT_TEST_RUN', False))


def _set_test_run():
    os.environ['DISENT_TEST_RUN'] = 'True'


# ========================================================================= #
# seeds                                                                     #
# ========================================================================= #


def seed(long=777):
    """
    https://pytorch.org/docs/stable/notes/randomness.html
    """
    if long is None:
        log.warning(f'[SEEDING]: no seed was specified. Seeding skipped!')
        return
    torch.manual_seed(long)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(long)
    log.info(f'[SEEDED]: {long}')


class TempNumpySeed(object):
    def __init__(self, seed=None, offset=0):
        if seed is not None:
            try:
                seed = int(seed)
            except:
                raise ValueError(f'{seed=} is not int-like!')
        self._seed = seed
        if seed is not None:
            self._seed += offset
        self._state = None

    def __enter__(self):
        if self._seed is not None:
            self._state = np.random.get_state()
            np.random.seed(self._seed)

    def __exit__(self, *args, **kwargs):
        if self._seed is not None:
            np.random.set_state(self._state)
            self._state = None

# ========================================================================= #
# IO                                                                        #
# ========================================================================= #


def to_numpy(array) -> np.ndarray:
    """
    Handles converting any array like object to a numpy array.
    specifically with support for a tensor
    """
    # TODO: replace... maybe with kornia
    if torch.is_tensor(array):
        return array.cpu().detach().numpy()
    # recursive conversion
    # not super efficient but allows handling of PIL.Image and other nested data.
    elif isinstance(array, (list, tuple)):
        return np.stack([to_numpy(elem) for elem in array], axis=0)
    else:
        return np.array(array)


# ========================================================================= #
# IO                                                                        #
# ========================================================================= #


def atomic_save(obj, path):
    """
    Save a model to a file, making sure that the file will
    never be partly written.

    This prevents the model from getting corrupted in the
    event that the process dies or the machine crashes.

    FROM: my obstacle_tower project
    """
    import os
    import torch

    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(obj, path + '.tmp')
    os.rename(path + '.tmp', path)


def save_model(model, path):
    atomic_save(model.state_dict(), path)
    log.info(f'[MODEL]: saved {path}')


def load_model(model, path, cuda=True, fail_if_missing=True):
    """
    FROM: my obstacle_tower project
    """
    import os
    import torch

    if path and os.path.exists(path):
        model.load_state_dict(torch.load(
            path,
            map_location=torch.device('cuda' if cuda else 'cpu')
        ))
        log.info(f'[MODEL]: loaded {path} (cuda: {cuda})')
    else:
        if fail_if_missing:
            raise Exception(f'Could not load model, path does not exist: {path}')
    if cuda:
        model = model.cuda()  # this needs to stay despite the above.
        log.info('[MODEL]: Moved to GPU')
    return model


# ========================================================================= #
# Iterators                                                                 #
# ========================================================================= #


def chunked(arr, chunk_size: int, include_remainder=True):
    """
    return an array of array chucks of size chunk_size.
    This is NOT an iterable, and returns all the data.
    """
    size = (len(arr) + chunk_size - 1) if include_remainder else len(arr)
    return [arr[chunk_size*i:chunk_size*(i+1)] for i in range(size // chunk_size)]


def iter_chunks(items, chunk_size: int, include_remainder=True):
    """
    iterable version of chunked.
    that does not evaluate unneeded elements
    """
    items = iter(items)
    for first in items:
        chunk = [first, *islice(items, chunk_size-1)]
        if len(chunk) >= chunk_size or include_remainder:
            yield chunk


def iter_rechunk(chunks, chunk_size: int, include_remainder=True):
    """
    takes in chunks and returns chunks of a new size.
    - Does not evaluate unneeded chunks
    """
    return iter_chunks(
        (item for chunk in chunks for item in chunk),  # flatten chunks
        chunk_size=chunk_size,
        include_remainder=include_remainder
    )


# TODO: not actually an iterator
def map_all(fn, *arg_lists, starmap: bool = True, collect_returned: bool = False, common_kwargs: dict = None):
    assert arg_lists, 'an empty list of args was passed'
    # check all lengths are the same
    num = len(arg_lists[0])
    assert num > 0
    assert all(len(items) == num for items in arg_lists)
    # update kwargs
    if common_kwargs is None:
        common_kwargs = {}
    # map everything
    if starmap:
        results = (fn(*args, **common_kwargs) for args in zip(*arg_lists))
    else:
        results = (fn(args, **common_kwargs) for args in zip(*arg_lists))
    # zip everything
    if collect_returned:
        return tuple(zip(*results))
    else:
        return tuple(results)


def collect_dicts(results: List[dict]):
    # collect everything
    keys = results[0].keys()
    values = zip(*([result[k] for k in keys] for result in results))
    return {k: list(v) for k, v in zip(keys, values)}


# TODO: this shouldn't be here
def aggregate_dict(results: dict, reduction='mean'):
    assert reduction == 'mean', 'mean is the only mode supported'
    return {
        k: sum(v) / len(v) for k, v in results.items()
    }


# ========================================================================= #
# STRINGS                                                                   #
# ========================================================================= #


def make_separator_str(text, header=None, width=100, char_v='#', char_h='=', char_corners=None):
    """
    function wraps text between two lines or inside a box with lines on either side.
    FROM: my obstacle_tower project
    """
    if char_corners is None:
        char_corners = char_v
    assert len(char_v) == len(char_corners)
    assert len(char_h) == 1
    import textwrap
    import pprint

    def append_wrapped(text):
        for line in text.splitlines():
            for wrapped in (textwrap.wrap(line, w, tabsize=4) if line.strip() else ['']):
                lines.append(f'{char_v} {wrapped:{w}s} {char_v}')

    w = width-4
    lines = []
    sep = f'{char_corners} {char_h*w} {char_corners}'
    lines.append(f'\n{sep}')
    if header:
        append_wrapped(header)
        lines.append(sep)
    if type(text) != str:
        text = pprint.pformat(text, width=w)
    append_wrapped(text)
    lines.append(f'{sep}\n')
    return '\n'.join(lines)


def make_box_str(text, header=None, width=100, char_v='|', char_h='-', char_corners='#'):
    """
    like print_separator but is isntead a box
    FROM: my obstacle_tower project
    """
    return make_separator_str(text, header=header, width=width, char_v=char_v, char_h=char_h, char_corners=char_corners)


def concat_lines(*strings, sep=' | '):
    """
    Join multi-line strings together horizontally, with the
    specified separator between them.
    """

    def pad_width(lines):
        max_len = max(len(line) for line in lines)
        return [f'{s:{max_len}}' for s in lines]

    def pad_height(list_of_lines):
        max_lines = max(len(lines) for lines in list_of_lines)
        return [(lines + ([''] * (max_lines - len(lines)))) for lines in list_of_lines]

    list_of_lines = [str(string).splitlines() for string in strings]
    list_of_lines = pad_height(list_of_lines)
    list_of_lines = [pad_width(lines) for lines in list_of_lines]
    return '\n'.join(sep.join(rows) for rows in zip(*list_of_lines))


# ========================================================================= #
# Iterable                                                                  #
# ========================================================================= #


class LengthIter(Sequence):

    def __iter__(self):
        # this takes priority over __getitem__, otherwise __getitem__ would need to
        # raise an IndexError if out of bounds to signal the end of iteration
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        raise NotImplemented()

    def __getitem__(self, item):
        raise NotImplemented()


# ========================================================================= #
# Context Manager Timer                                                     #
# ========================================================================= #


class Timer:
    def __init__(self, print_name=None, log_level=logging.INFO):
        self._start_time: int = None
        self._end_time: int = None
        self._print_name = print_name
        self._log_level = log_level

    def __enter__(self):
        self._start_time = time.time_ns()
        return self

    def __exit__(self, *args, **kwargs):
        self._end_time = time.time_ns()
        if self._print_name:
            log.log(self._log_level, f'{self._print_name}: {self.pretty}')

    @property
    def elapsed_ns(self) -> int:
        if self._start_time is None:
            return 0
        if self._end_time is None:
            return time.time_ns() - self._start_time
        return self._end_time - self._start_time

    @property
    def elapsed_ms(self) -> float:
        return self.elapsed_ns / 1_000_000

    @property
    def elapsed(self) -> float:
        return self.elapsed_ns / 1_000_000_000

    @property
    def pretty(self) -> str:
        return Timer.prettify_time(self.elapsed_ns)

    def __int__(self): return self.elapsed_ns
    def __float__(self): return self.elapsed
    def __str__(self): return self.pretty
    def __repr__(self): return self.pretty

    @staticmethod
    def prettify_time(ns: int) -> str:
        if ns == 0:
            return 'N/A'
        elif ns < 0:
            return 'NaN'
        # get power of 1000
        pow = min(3, int(np.log10(ns) // 3))
        time = ns / 1000**pow
        # get pretty string!
        if pow < 3 or time < 60:
            # less than 1 minute
            name = ['ns', 'µs', 'ms', 's'][pow]
            return f'{time:.3f}{name}'
        else:
            # 1 or more minutes
            s = int(time)
            d, s = divmod(s, 86400)
            h, s = divmod(s, 3600)
            m, s = divmod(s, 60)
            if d > 0:   return f'{d}d:{h}h:{m}m'
            elif h > 0: return f'{h}h:{m}m:{s}s'
            else:       return f'{m}m:{s}s'


# ========================================================================= #
# Function Helper                                                           #
# ========================================================================= #


def wrapped_partial(func, *args, **kwargs):
    """
    Like functools.partial but keeps the same __name__ and __doc__
    on the returned function.
    """
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    return partial_func


# ========================================================================= #
# Memory Usage                                                              #
# ========================================================================= #


def get_memory_usage():
    import os
    import psutil
    process = psutil.Process(os.getpid())
    num_bytes = process.memory_info().rss  # in bytes
    return num_bytes


# ========================================================================= #
# Torch Helper                                                              #
# ========================================================================= #


class DisentModule(torch.nn.Module):

    def _forward_unimplemented(self, *args):
        # Annoying fix applied by torch for Module.forward:
        # https://github.com/python/mypy/issues/8795
        raise RuntimeError('This should never run!')

    def forward(self, *args, **kwargs):
        raise NotImplementedError


class DisentLightningModule(pl.LightningModule):

    def _forward_unimplemented(self, *args):
        # Annoying fix applied by torch for Module.forward:
        # https://github.com/python/mypy/issues/8795
        raise RuntimeError('This should never run!')


class DisentConfigurable(object):

    @dataclass
    class cfg(object):
        def get_keys(self) -> list:
            return list(self.to_dict().keys())

        def to_dict(self) -> dict:
            return asdict(self)

        def __str__(self):
            return pformat(self.to_dict(), sort_dicts=False)

    def __init__(self, cfg: cfg = cfg()):
        if cfg is None:
            cfg = self.__class__.cfg()
            log.info(f'Initialised default config {cfg=} for {self.__class__.__name__}')
        super().__init__()
        assert isinstance(cfg, self.__class__.cfg), f'{cfg=} ({type(cfg)}) is not an instance of {self.__class__.cfg}'
        self.cfg = cfg


# ========================================================================= #
# Slot Tuple                                                                #
# ========================================================================= #


@dataclass
class TupleDataClass:
    """
    Like a named tuple + dataclass combination, that is mutable.
    -- requires that you still decorate the inherited class with @dataclass
    """

    __field_names_cache = None

    @property
    def __field_names(self):
        # check for attribute and set on class only
        if self.__class__.__field_names_cache is None:
            self.__class__.__field_names_cache = tuple(f.name for f in fields(self))
        return self.__class__.__field_names_cache

    def __iter__(self):
        for name in self.__field_names:
            yield getattr(self, name)

    def __len__(self):
        return self.__field_names.__len__()

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(f"{name}={repr(getattr(self, name))}" for name in self.__field_names)})'


# ========================================================================= #
# END                                                                       #
# ========================================================================= #


def debug_transform_tensors(obj):
    """
    recursively convert all tensors to their shapes for debugging
    """
    if isinstance(obj, (torch.Tensor, np.ndarray)):
        return obj.shape
    elif isinstance(obj, dict):
        return {debug_transform_tensors(k): debug_transform_tensors(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return list(debug_transform_tensors(v) for v in obj)
    elif isinstance(obj, tuple):
        return tuple(debug_transform_tensors(v) for v in obj)
    elif isinstance(obj, set):
        return {debug_transform_tensors(k) for k in obj}
    else:
        return obj


def pprint_tensors(*args, **kwargs):
    print(*(debug_transform_tensors(arg) for arg in args), **kwargs)


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
