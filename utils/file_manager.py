# -*- coding: utf-8 -*-
import re
import os
import json
import fnmatch
from pathlib import Path
from typing import Any, Union, Dict
from _ctypes import PyObj_FromPtr
from datetime import datetime


def get_list_file(pattern, directory: str) -> list:
    """To get file list with the good pattern in the directory

    Args:
        pattern ([str]): Set pattern filter (ex : '*.py', '????.??.txt')
        directory ([str]): Set search directory
    Returns:
        [list]: return the files that match the pattern
    """
    files = fnmatch.filter(os.listdir(directory), pattern)
    return files


def check_dates_window(current_time: str, start: str, end: str, format: str = '%Y-%m-%d',
                       min_date: str = '1971-01-01',  max_date: str = '2099-01-01') -> bool:
    """Checks if the time is between start and end
       Put '' if no start or end date , it will be replaced by min_date and max_date
       
    :param current_time: set the time to test
    :type current_time: str
    :param start: set the start time
    :type start: str
    :param end: set the end time
    :type end: str
    :param format: the format of the time, defaults to %Y-%m-%d'
    :type format: str, optional
    :param min_date: Set the min date, defaults to 1971-01-01'
    :type min_date: str, optional
    :param max_date: Set the max date, defaults to 2099-01-01'
    :type max_date: str, optional
    :return: return true if the current time is between start and end
    :rtype: bool
    """
    if start == '':
        t_start = datetime.strptime(min_date, format)
    else:
        t_start = datetime.strptime(start, format)
    if end == '':
        t_end = datetime.strptime(max_date, format)
    else:
        t_end = datetime.strptime(end, format)

    t_current = datetime.strptime(current_time, '%Y.%j')
    return t_start <= t_current <= t_end


def scan_dir(directory: str,
             net: str ='*', sta: str ='*',
             loc: str ='*', cha: str ='*',
             year: str ='*', day: str ='*',
             quality: str ='*') -> dict:
    """To get dict for each file in the sds
       - name file is the key
       Information for each files is:
           - the name
           - absolute path
           - size
           - last modification

    :param dir: Set search directory
    :type dir: str
    :return: return dict with files that match the pattern
    :rtype: dict
    """
    file_in_dir = {}
    for path in Path(directory).rglob(f'{net}.{sta}.{loc}.{cha}.{quality}.{year}.{day}'):      #net.sta.loc.cha.D.year.day
        if test_mseed_sds_name_format(path):
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


def check_pattern(str_to_test, pattern):
    # TODO finir
    if pattern == "*":
        return True
    #elif pattern:
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


def test_mseed_sds_name_format(path: Path):
    """
    To test if the name has a good format
    """
    match = re.search(
        r"[A-Z0-9]{1,2}\.[A-Z0-9]{1,5}\.[0-9]{0,2}\.[A-Z0-9]{1,3}\.[A-Z]{1}\.[0-9]{4}\.[0-9]{1,3}",
        path.name)
    return match


def test_network_format(network: str) -> re:
    """
    To test if the network has a good format
    """
    if 1 <= len(network) <= 2:
        match = re.search(
            r"[A-Z0-9]{1,2}",
            network)
        return bool(match)
    else: # TODO return erreur or log file
        return False


def test_station_format(station: str) -> re:
    """
    To test if the station has a good format
    """
    if 1 <= len(station) <= 5:
        match = re.search(
            r"[A-Z0-9]{1,5}",
            station)
        return match
    else: # TODO return erreur or log file
        return False


def test_channel_format(channel: str) -> re:
    """
    To test if the channel has a good format
    """
    if 1 <= len(channel) <= 3:
        match = re.search(
            r"[A-Z0-9]{1,3}",
            channel)
        return match
    else:   # TODO return erreur or log file
        return False


def test_location_format(location: str) -> re:
    """
    To test if the location has a good format
    """
    if 0 <= len(location) <= 2:
        match = re.search(
            r"[0-9]{0,2}",
            location)
        return match
    else:    # TODO return erreur or log file
        return False


def write_json(data, filename: str) -> None:
    """To save list or dict in json file

    Args:
        data ([list] or [dict]): data to save
        filename ([str])       : set the file name
    """
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value

class MyEncoder(json.JSONEncoder): 
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr


def write_json_scan(data, filename: str) -> None:
    """To save list or dict in json file

    Arg
        data ([list] or [dict]): data to save
        filename ([str])       : set the file name
    """
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(data))
        
        
def load_json(json_filename: str) -> Union[list, dict]:
    """
    Load a JSON from a given filename

    json_filename -- The filename to load

    return        -- The JSON loaded from filename
    """
    result = json.load(open(json_filename, 'r'))
    return result


def create_dir(new_dir_path: str) -> str:
    """Takes the path as input and creates all missing directories in the path,
       including the parent directory

    :param new_path: set new path
    :type new_path: str
    """
    path = Path(new_dir_path)
    path.mkdir(parents=True, exist_ok=True)


def get_parents_path(path: str) -> str:
    """Get parents path

    :param path: set path of file
    :type path: str
    :return: return parent path
    :rtype: str
    """
    current_path = Path(path)
    return str(current_path.parents[0])


def create_parent_dir(new_file_path: str) -> str:
    """Takes the file path as input and creates all missing directories in the path,
       including the parent directory

    :param new_path: set new path
    :type new_path: str
    """
    parents_path = get_parents_path(new_file_path)
    path = Path(parents_path)
    path.mkdir(parents=True, exist_ok=True)