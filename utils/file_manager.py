# -*- coding: utf-8 -*-
import re
import os
import json
import fnmatch
from pathlib import Path


def get_list_file(patern, directory: str) -> list:
    """To get file list with the good patern in the directory

    Args:
        patern ([str]): Set patern filter (ex : '*.py', '????.??.txt')
        directory ([str]): Set search directory
    Returns:
        [list]: return the files that match the pattern
    """
    files = fnmatch.filter(os.listdir(directory), patern)
    return files


def scan_dir(directory: str) -> dict:
    """To get dict for each file in the sds
       - name file is the key
       Inforations for each files is:
           - the name
           - absolute path
           - size
           - last modification

    Args:
        directory ([str]): Set search directory
    Returns:
        [dict]: return dict with files that match the pattern
    """
    file_in_dir = {}
    for path in Path(directory).rglob('*.*.*.*.*.*.*'):
        if test_name_format(path) and in_white_list(path):
            stat_file = os.stat(path.absolute())
            infos = path.name.split('.')
            file_in_dir[path.name] = {'name': path.name,
                                      'abs_path': str(path.absolute()),
                                      'size': stat_file.st_size,
                                      'last_m': stat_file.st_mtime,
                                      'info' : {'network' : infos[0],
                                                'station' : infos[1],
                                                'location': infos[2],
                                                'channel' : infos[3],
                                                'quality' : infos[4],
                                                'year'    : infos[5],
                                                'day'     : infos[6]}
                                      }
    return file_in_dir


def check_pattern(str_to_test, pattern):
    if pattern == "*":
        return True
    elif pattern:
    else:
        return False
    #pattern = r"ojhiu."
    #test = "ojhiuh"
    #if re.match(pattern, test):
    #    print("ok")


def get_infos_with_name(path):
    # TODO doc
    list_infos = path.name.split('.')
    return list_infos[0], list_infos[1], list_infos[2], list_infos[3], list_infos[5], list_infos[6]

def in_white_list(path, net_pattern='*', station_pattern='*', location_pattern='*', channel_pattern='*', pattern_year='*'):
    # TODO finir
    network, station, location, channel, year = get_infos_with_name(path)
    if check_pattern(network, net_pattern) and\
       check_pattern(station, station_pattern) and\
       check_pattern(channel, channel_pattern) and\
       check_pattern(year, pattern_year):
        return True
    else:
        return False

def test_name_format(path):
    """
    To test if the name has a good format
    """
    match = re.search(
        r"[A-Z0-9]{1,2}\.[A-Z0-9]{1,5}\.[0-9]{0,2}\.[A-Z0-9]{1,3}\.[A-Z]{1}\.[0-9]{4}\.[0-9]{1,3}",
        path.name)
    return match


def write_json(data, filename: str) -> None:
    """To save list or dict in json file

    Args:
        data ([list] or [dict]): data to save
        filename ([str])       : set the file name
    """
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))


def load_json(json_filename):
    """
    Load a JSON from a given filename

    json_filename -- The filename to load

    return        -- The JSON loaded from filename
    """
    result = json.load(open(json_filename, 'r'))
    return result


def create_dir(new_path):
    """Takes the path as input and creates all missing directories in the path,
       including the parent directory
    Args:
        new_path ([type]): [description]
    """
    path = Path(new_path)
    path.mkdir(parents=True, exist_ok=True)

