#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Ambrois David
# Created Date: 2021/04/01
# version = '0.1'
# ---------------------------------------------------------------------------
"""repack_data.py: Repack mseed data."""
# ---------------------------------------------------------------------------
import os
import obspy
import json
from pathlib import Path
from os.path import relpath
# ---------------------------------------------------------------------------


def get_parents_path(path):
    """
    Get parents path
    """
    current_path = Path(path)
    return str(current_path.parents[0])


def create_dir(new_path):
    """Takes the path as input and creates all missing directories in the path,
       including the parent directory
    Args:
        new_path ([type]): [description]
    """
    parents_path = get_parents_path(new_path)
    path = Path(parents_path)
    path.mkdir(parents=True, exist_ok=True)


def scan_dir(dir):
    file_in_dir = {}
    for path in Path(dir).rglob('*.*.*.*.*.*.*'):
        st = os.stat(path.absolute())
        file_in_dir[path.name] = {'name': path.name,
                                  'abs_path': str(path.absolute()),
                                  'path_in_sds': relpath(str(path.absolute()), dir),
                                  'size': st.st_size,
                                  'last_m': st.st_mtime}
    return file_in_dir


def repack_mseed_file(mseed_file, output, new_size):
    """
    """
    #print(mseed_file)
    st = obspy.read(mseed_file)
    st.write(output, format="MSEED", reclen=new_size)


def main(old_sds, new_sds, pack_size=512):
    """
    1) List file in sds
    2) Repack mseed file
    3) Save in other sds
    """
    list_in_sds = scan_dir(old_sds)
    #with open('data.json', 'w') as f:
    #    json.dump(list_in_sds, f)
    for key in list_in_sds.keys():
        try:
            mseed = list_in_sds[key]
            create_dir(os.path.join(new_sds , mseed['path_in_sds']))
            repack_mseed_file(mseed['abs_path'], os.path.join(new_sds , mseed['path_in_sds']), pack_size)
        except:
            print(key)


if __name__ == '__main__':
    main('SDS_4096', 'SDS_512')