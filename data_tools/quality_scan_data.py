#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Ambrois David
# Created Date: 2021/04/25
# version = '0.1'
# ---------------------------------------------------------------------------
"""Calculate stat data and save in SQS (Seed Quality Structure)."""
# ---------------------------------------------------------------------------
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.join(SCRIPT_DIR, '..', 'utils')))
# ---------------------------------------------------------------------------
import argparse
from utils.file_manager import create_dir, load_json, scan_dir, check_seed_format, write_json


FILE_ANALYSE_PATH = "/Users/ambrois/Documents/01_Scripts/slinkgo/file-analyse/file-analyse"


def process_scan(program_scan_path, mseed_file, year, day, sensitivity=1, ws=600, output="output.json", verbose=False):
    """
      -d int
        	Set the processed julian day (1-366)
      -gap float
        	Set the minimal gap size in term of inter sample (default 1.5)
      -i string
        	MSeed input file
      -o string
        	Statistics output file (default "output.json")
      -sensitivity float
        	Set the channel global sensitivity (default 1)
      -v	Set verbose flag
      -ws int
        	Set the metrics computation size (default 86400)
      -y int
        	Set the processed year
    """
    arg_cmd = [program_scan_path]

    arg_cmd += ["-i", mseed_file]         # Input

    arg_cmd += ["-d", day]

    arg_cmd += ["-y", year]
    
    arg_cmd += ["-ws", ws]
    
    arg_cmd += ["-sensitivity", sensitivity]
    
    if verbose:
        arg_cmd += ["-v"]

    arg_cmd +=  ["-o" , output]
    os.system(' '.join([str(x) for x in arg_cmd]))


def save_result(input, output, sds_path):
    # TODO add stats file (size, modification, droits)
    scan_data = load_json(input)
    data_metrics = scan_data["DataMetrics"]
    
    min = []
    max = []
    avg = []
    stddev = []
    rms = []
    time = []
    
    for window_metrics in data_metrics:
    
        min.append(window_metrics["min"])
        max.append(window_metrics["max"])
        avg.append(window_metrics["avg"])
        stddev.append(window_metrics["stddev"])
        rms.append(window_metrics["rms"])
        time.append(window_metrics["data_start_time"])
        
    data = {'starttime':time[0],
            'windows_size': scan_data["WindowSize"],
            'gap': scan_data["Gap"],
            'overlap': scan_data["Overlap"],
            'GeneratedTime': scan_data["GeneratedTime"],
            'sds_path': sds_path,
            'data_metrics':{
                            'min': min,
                            'max': max,
                            'avg': avg,
                            'stddev': stddev,
                            'rms': rms,
                            'time':time,
                           }
            }
    
    write_json(data, output)


def get_config(cfg_file):
    """Extract infos in cfg file

    :param cfg_file: Set the config file
    :type cfg_file: str
    """
    return load_json(cfg_file)


def get_dict_info(info):
    
    network = info['network']
    station = info['station']
    location= info['location']
    channel = info['channel']
    channel_quality = f"{channel}.{info['quality']}"
    
    return {'path_in_sqs': os.path.join(info['year'] ,network , station, channel_quality),
            'name': f"{network}.{station}.{location}.{channel_quality}.{info['year']}.{info['day']}",
            'network': network,
            'station': station,
            'location': location,
            'channel': channel}


def main():
    parser = argparse.ArgumentParser(description="Calcul quality stat data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-conf", type=str, help="Set input file")
    parser.add_argument("-sds", type=str, help="Set SDS path")
    parser.add_argument("-sqs", type=str, help="Set SQS path")
    #parser.add_argument("-erase", default=False, action="store_true", help="Erase old data")
    args = parser.parse_args()
    
    list_conf = get_config(args.conf)
    print(list_conf)
    for current_conf in list_conf:
        sta = current_conf['sta']
        net = current_conf['net']
        cha = current_conf['cha']
        loc = current_conf['loc']
        year = current_conf['year']
        
           
        list_in_sds = scan_dir(os.path.join(args.sds),
                                   net=net, sta=sta,
                                   loc=loc, cha=cha, 
                                   year=year)
    
        for key, values in list_in_sds.items():
            if args.verbose:
                print(f"Process file : {key}")
            infos = get_dict_info(values['info'])
            if check_seed_format(infos): # TODO maybe to do the verification before begins the process
                create_dir(os.path.join(args.sqs, infos["path_in_sqs"]))
                output = os.path.join(args.sqs, infos['path_in_sqs'], infos['name'])+'.json'
                if not os.path.isfile(output):
                    day = values['name'].split('.')[-1]
                    year = values['name'].split('.')[-2]
                    process_scan(FILE_ANALYSE_PATH,
                                 values['abs_path'],
                                 year,
                                 day,
                                 ws=600,
                                 output="tmp_output.json",
                                 verbose=False,
                                 sensitivity=1)
                    try:
                        save_result("tmp_output.json", output, values['abs_path'])
                        os.remove("tmp_output.json")
                    except FileNotFoundError as e:
                        print(f"{e} : Error during Scan")
                else:
                    print(f"{output} already exist, next file")
            else:
                print(f"Does not respect the seed format: {infos}")
    
if __name__ == '__main__':
    main()