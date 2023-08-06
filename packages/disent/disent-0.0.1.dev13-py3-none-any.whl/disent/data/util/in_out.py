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

import logging
import warnings


log = logging.getLogger(__name__)

# ========================================================================= #
# io                                                                        #
# ========================================================================= #


def ensure_dir_exists(*path, is_file=False, absolute=False):
    import os
    # join path
    path = os.path.join(*path)
    # to abs path
    if absolute:
        path = os.path.abspath(path)
    # remove file
    dirs = os.path.dirname(path) if is_file else path
    # create missing directory
    if os.path.exists(dirs):
        if not os.path.isdir(dirs):
            raise IOError(f'path is not a directory: {dirs}')
    else:
        os.makedirs(dirs, exist_ok=True)
        log.info(f'created missing directories: {dirs}')
    # return directory
    return path


def ensure_parent_dir_exists(*path):
    return ensure_dir_exists(*path, is_file=True, absolute=True)


def basename_from_url(url):
    import os
    from urllib.parse import urlparse
    return os.path.basename(urlparse(url).path)


def download_file(url, save_path=None, overwrite_existing=False, chunk_size=4096):
    import requests
    import os
    from tqdm import tqdm

    if save_path is None:
        save_path = basename_from_url(url)
        log.info(f'inferred save_path="{save_path}"')

    # split path
    # TODO: also used in base.py for processing, convert to with syntax.
    path_dir, path_base = os.path.split(save_path)
    ensure_dir_exists(path_dir)

    if not path_base:
        raise Exception('Invalid save path: "{save_path}"')

    # check save path isnt there
    if os.path.isfile(save_path):
        if overwrite_existing:
            warnings.warn(f'Overwriting existing file: "{save_path}"')
        else:
            raise Exception(f'File already exists: "{save_path}" set overwrite_existing=True to overwrite.')

    # we download to a temporary file in case there is an error
    temp_download_path = os.path.join(path_dir, f'.{path_base}.download.temp')

    # open the file for saving
    with open(temp_download_path, "wb") as file:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        # cast to integer if content-length exists on response
        if total_length is not None:
            total_length = int(total_length)

        # download with progress bar
        with tqdm(total=total_length, desc=f'Downloading "{path_base}"', unit='B', unit_scale=True, unit_divisor=1024) as progress:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.update(chunk_size)

    # remove if we can overwrite
    if overwrite_existing and os.path.isfile(save_path):
        # TODO: is this necessary?
        os.remove(save_path)

    # rename temp download
    os.rename(temp_download_path, save_path)


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
