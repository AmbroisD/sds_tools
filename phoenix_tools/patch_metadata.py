# -*- coding: utf-8 -*-

# This program use the program check_metadata to patch the station xml files

import os
import json
import xmltodict
from typing import Any, Dict, List
from obspy import read_inventory
from collections import OrderedDict
#"../../../00_Projets/01_Ecuador/inventory/Equateur_20220610/2J_PAC2.xml"


def inv2dict(filename: str) -> Dict[Any, Any]:
    """convert the inventory station to a dictionary

    :param filename: Set filename of the inventory station
    :type filename: str
    :return: Returns a dictionary of the inventory station
    :rtype: dict
    """
    return xmltodict.parse(open(filename, 'r').read())


def dict2inv(dict_inv: Dict[Any, Any], output_filename: str) -> None:
    """Converts and save a inventory station dictionary in xml file.

    :param dict_inv: Set dictionary of inventory station
    :type dict_inv: dict
    :param output_filename: Set the output filename
    :type output_filename: str
    """
    xml = xmltodict.unparse(dict_inv)
    with open(output_filename, "w") as f:
        f.write(xml)

#channel = 'XXX'
#location = '00'
#lat = '-1.064875'
#lon = '-2.064875'
#elev = '311'
#depth = '0.5'
#start = '2001-09-01T00:00:00Z'
#end = '2002-12-02T00:00:00Z'


def add_channel(dict_inv: Dict[Any, Any], channel: str, 
                location: str, start: str, end: str, 
                lat: str, lon: str, elev: str, depth: str) -> Dict[Any, Any]:
    """Add a channel in inventory station dictionary"""
    
    new = OrderedDict([('@code', channel),
                       ('@startDate', start),
                       ('@endDate', end),
                       ('@locationCode', location),
                       ('Latitude', lat),
                       ('Longitude', lon),
                       ('Elevation', elev),
                       ('Depth', depth),
                       ('Azimuth', '90'),
                       ('Dip', '0'),
                       ('Type', ['CONTINUOUS', 'GEOPHYSICAL'])])

    dict_inv['FDSNStationXML']['Network']['Station']['Channel'].append(new)
    return dict_inv


def get_period_channel_missing_list(station: str, dirname: str) -> List:
    """
    return a list of channel names that are missing from the sds/metadata comparaison

    :param station: Set station name
    :type station: str
    :param dirname: Set directory name with json information
    :type dirname: str
    :return: Returns list of the channel names that are missing from the sds/metadata
    :rtype: list
    """
    return json.loads(open(os.path.join(dirname, station)+".json", "r").read())


def main(station, dir_metadata, dir_json):
    #for xml_file in os.listdir(os.path.dirname()):
    dict_inv = inv2dict(os.path.join(dir_metadata, "Z2_HBAR.xml"))
    list_miss = get_period_channel_missing_list(station, dir_json)
    for channel_missing in list_miss:
        dict_inv = add_channel(dict_inv, channel_missing[2], channel_missing[1], 
                               channel_missing[3], channel_missing[4], 
                               1, 1, 1, 1)
        
    dict2inv(dict_inv, "text.xml")


if __name__ == '__main__':
    main("HBAR", "./metadata", "./stations_json")