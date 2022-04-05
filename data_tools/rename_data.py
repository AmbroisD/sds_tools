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
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.join(SCRIPT_DIR, '..', 'utils')))
# ---------------------------------------------------------------------------
import argparse
import subprocess
from pathlib import Path
from os.path import relpath
from typing import Any, Dict
from utils.file_manager import load_json, create_dir, check_dates_window, scan_dir
from utils.file_manager import test_channel_format, test_location_format,\
                               test_network_format, test_station_format
#from ..utils.file_manager import test_mseed_sds_name_format
# ---------------------------------------------------------------------------

GSMOD_PATH = "/Users/ambrois/Documents/01_Scripts/slinkgo/gmsmod"
MAXDATES = "2022-01-01"

def process_file(mseed_file, output, sta = None, net = None, loc = None, cha = None):
    """    To rename mseed file
           Use gmsmod to repack with good velocity  

        Help for gmsmod:
            -channel string      Set the new channel code
            -i string            MSeed input file
            -location string     Set the new location code (default "not set")
            -network string      Set the new network code
            -o string            The modified mseed file version (default "output.mseed")
            -station string      Set the new station code

    :param mseed_file: Set mseed file
    :type mseed_file: str
    :param output: Set output name
    :type output: str
    :param parameters: new name
    :type parameters: dict
    """
    # Build cmd line
    arg_cmd = [os.path.join(GSMOD_PATH, "gmsmod")]

    arg_cmd += ["-i", mseed_file]         # Input

    if sta is not None:                   # Station
        arg_cmd += ["-station", sta]
    if net is not None:                   # Network
        arg_cmd += ["-network", net]
    if loc is not None:                   # Location Code
        arg_cmd += ["-location", loc]
    if cha is not None:                   # Channel
        arg_cmd += ["-channel", cha]

    arg_cmd +=  ["-o" , output]           # Output

    output = subprocess.run(arg_cmd,
                            capture_output=True)
    # UPGRADE  read output result


def get_config(cfg_file):
    """Extract infos in cfg file

    :param cfg_file: Set the config file
    :type cfg_file: str
    """
    return load_json(cfg_file)


def check_seed_format(new_infos: Dict[Any, Any]) -> bool:
    """Check the seed format

    :param new_infos: Set dict with new infos
    :type new_infos: dict
    :return: return True if the seed format is good.
    :rtype: bool
    """
    return test_station_format(new_infos['station']) and\
           test_network_format(new_infos['network']) and\
           test_location_format(new_infos['location']) and\
           test_channel_format(new_infos['channel'])


def get_new_infos(info: Dict[Any, Any], new: list) -> dict:
    """Generate path in SDS and new stream info

    :param info: Infos of mseed file
    :type info: dict
    :param new: New name info
    :type new: list
    :return: return new_info
    :rtype: str
    """
    if new[0] == '*':
        network = info['network']
    else:
        network = new[0]

    if new[1] == '*':
        station = info['station']
    else:
        station = new[1]

    if new[2] == '*':
        location= info['location']
    else:
        location = new[2]

    if new[3] == '*':
        channel = f"{info['channel']}"
        channel_quality = f"{info['channel']}.{info['quality']}"
    else:
        channel = f"{new[3]}"
        channel_quality = f"{new[3]}.{info['quality']}"

    return {'new_path': os.path.join(info['year'] ,network , station, channel_quality),
            'name': f"{network}.{station}.{location}.{channel_quality}.{info['year']}.{info['day']}",
            'network': network,
            'station': station,
            'location': location,
            'channel': channel}


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
 
    list_conf = get_config(args.conf)
    for current_conf in list_conf:
        old = current_conf['old']
        new = current_conf['new']
        date = current_conf['date']
        list_in_sds = scan_dir(os.path.join(args.sds), # TODO year add
                               net=old[0], sta =old[1],
                               loc=old[2], cha=old[3])
        for key, values in list_in_sds.items():
            if args.verbose:
                print(f"Process file : {key}")
            if check_dates_window(f"{values['info']['year']}.{values['info']['day']}", date['start'], date['end'], max_date=MAXDATES):
                new_infos = get_new_infos(values['info'], new)
                if True: #check_seed_format(new_infos): # TODO maybe to do the verification before begins the process
                    create_dir(os.path.join(args.sds, new_infos["new_path"]))
                    output = os.path.join(args.sds, new_infos['new_path'], new_infos['name'])
                    if not os.path.isfile(output):
                        process_file(values['abs_path'],
                                     output,
                                     sta = new_infos['station'],
                                     net = new_infos['network'],
                                     loc = new_infos['location'],
                                     cha = new_infos['channel'])
                    else:
                        print(f"{output} already exist, next file")
                else:
                    print(f"Does not respect the seed format: {new_infos}")

if __name__ == '__main__':
    main()