#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Ambrois David
# Created Date: 2022/06/15
# version = '0.1'
# ---------------------------------------------------------------------------
"""To Check if metadata exist for the data present in the SDS 
   and save result in SQS (Seed Quality Structure)."""
# ---------------------------------------------------------------------------
import os
from pickle import FALSE
import sys
from tabnanny import verbose
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.join(SCRIPT_DIR, '..', 'utils')))
# ---------------------------------------------------------------------------
import argparse
import itertools
from datetime import datetime
from check_metadata import MetaDataCheck
from utils.file_manager import create_dir, load_json, scan_dir, check_seed_format, write_json

VERBOSE = False
SDS="/Users/ambrois/Documents/01_Scripts/data/SDS_TEST"
LIST2VERIFY = ["ABAB", "ABH2", "ABLA", "ACHN", "ADUR", "ALBE",
               "ALIB", "AMNT", "AMTV", "ANUV", "APED", "APLA",
               "APO1", "APO2", "AQUE", "BALZ", "CABP", "CHIB",
               "CHIS", "FAEM", "FLFR", "GYE1", "GYE2", "GYE3",
               "GYEB", "ISPT", "JAMA", "LALU", "MAG1", "MILO",
               "MORR", "OB11", "OB12", "OB13", "OB14", "OB21",
               "OB22", "OB23", "OB24", "OB31", "OB32", "OB33",
               "OB34", "OB41", "OB42", "OB44", "OB51", "OB52",
               "OB53", "OJOA", "PAC2", "PACO", "PDNS", "PECV",
               "PPLP", "PUBA", "QUEV", "SALI", "SANA", "SANP",
               "SARA", "SEVS", "UNPA", "XAVI", "ZAPA"]


def get_file_list(station):
    return scan_dir(os.path.join(SDS), sta=station)

  
def intervals_extract(iterable):
# sequential number into intervals
      
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable),
    lambda t: t[1] - t[0]):
        group = list(group)
        yield [group[0][1], group[-1][1]]
  
    # Driver code
    #l = [2, 3, 4, 5, 7, 8, 9, 11, 15, 16]
    #print( list(intervals_extract(l)))


def resume_results(pb_station):
    f = open("resume_pb_station.txt", "w")
    for sta_k, stations in pb_station.items():
        for loc_k, loc in stations.items():
            for cha_k, channel in loc.items():
                for year_k, year in channel.items():
                    for period in list(intervals_extract(year)):
                        start = datetime.strptime(f"{year_k}.{period[0]}", "%Y.%j" )
                        end = datetime.strptime(f"{year_k}.{period[1]}", "%Y.%j" )
                        f.write(f"Station: {sta_k} | Location: {loc_k} | Channel: {cha_k} | Year: {year_k} | Start: {start} | End: {end}")
                        f.write('\n')


def add_new_error(pb_station: dict, station: str , location: str, channel: str, date: str):
    year, day = date.split('.')
    if not station in pb_station.keys():
        pb_station[station] = {}
    if not location in pb_station[station].keys():
        pb_station[station][location] = {}  
    if not channel in pb_station[station][location].keys():
        pb_station[station][location][channel]  = {}
    if not year in pb_station[station][location][channel].keys():
        pb_station[station][location][channel][year]  = []
    pb_station[station][location][channel][year].append(int(day))
    return pb_station


def main(station):
    pb_station = {}
    meta = MetaDataCheck(station=station)
    list_file = get_file_list(station)
    for _, file in list_file.items():
        location = file['info']['location']
        channel = file['info']['channel']
        date = f"{file['info']['year']}.{file['info']['day']}"
        if not meta.check_channel_period(location, channel, date):
            pb_station = add_new_error(pb_station, station, location, channel, date)
        else:
            if VERBOSE:
                print("ok")
    resume = resume_results(pb_station)
    write_json(resume, 'test_pheonix.json')
            
        
if __name__ == '__main__':
    #for sta in LIST2VERIFY:
    main("HBAR")