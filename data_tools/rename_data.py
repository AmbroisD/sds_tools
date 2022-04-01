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
import argparse
import subprocess
from pathlib import Path
from os.path import relpath
from utils.file_manager import load_json
from utils.file_manager import scan_dir
from utils.file_manager import create_parent_dir
from utils.file_manager import test_mseed_sds_name_format
# ---------------------------------------------------------------------------

GSMOD_PATH = "/Users/ambrois/Documents/01_Scripts/slinkgo/gmsmod"


def process_file(mseed_file, output, parameters={'sta':'*', 'net': '*', 'loc': '*', 'cha': '*'}):
    """    To rename mseed file
           Use gmsmod to repack with good velocity  

    :param mseed_file: Set mseed file
    :type mseed_file: str
    :param output: Set output name
    :type output: str
    :param parameters: new name
    :type parameters: dict
    """
    output = subprocess.run([os.path.join(GSMOD_PATH, "gmsmod"), "-R", new_size, "-o" , output, mseed_file], capture_output=True)
    # UPGRADE  read output result


def get_config(cfg_file):
    """Extrac infos in cfg file

    :param cfg_file: Set the config file
    :type cfg_file: str
    """
    return load_json(cfg_file)


def get_arg(param_station: dict) -> str:
    """return str with arg for gmsmod

    :param param_station: _description_
    :type param_station: dict
    """


def main():
    """
    1) List file in sds
    2) Rename mseed file
    3) Save in other sds
    """
    parser = argparse.ArgumentParser(description="Change header and name of mseed data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-conf", type=str, help="Set input file")
    parser.add_argument("-sds", type=str, help="Set SDS path")
    parser.add_argument("-erase", default=False, action="store_true", help="Erase old data")
    args = parser.parse_args()
    #args.y
 
    list_parameter = get_config(args.conf)
    for current_station in list_parameter:
        list_in_sds = scan_dir(args.sds, net='*', str ='*', loc='*', cha='*', start = None, end = None)
    
        for key in list_in_sds.keys():
            mseed = list_in_sds[key]
            create_parent_dir(os.path.join(new_sds , mseed['path_in_sds']))
            process_file(mseed['abs_path'], os.path.join(new_sds , mseed['path_in_sds']), get_arg(current_station))


if __name__ == '__main__':
    main()