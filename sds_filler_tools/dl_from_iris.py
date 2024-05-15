#!/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from urllib2 import urlopen
import os


SDS_SOURCE = '/data/archive'
SDS_DEST = '/data/keep_sds_archive'
IRIS = 'https://service.iris.edu/fdsnws/dataselect/1/query'
BEGIN_DATE = '2021.250'
END_DATE = '2021.254'
NETWORK_BLACKLIST = ['AM']


def main():
    t = datetime.strptime(BEGIN_DATE, '%Y.%j')
    year_path = os.path.join(SDS_SOURCE, str(t.year))
    d_year_path = os.path.join(SDS_DEST, str(t.year))
    for network_dir in os.listdir(year_path):
        if network_dir in NETWORK_BLACKLIST:
            continue
        network_path = os.path.join(year_path, network_dir)
        d_network_path = os.path.join(d_year_path, network_dir)
        for station_dir in os.listdir(network_path):
            station_path = os.path.join(network_path, station_dir)
            d_station_path = os.path.join(d_network_path, station_dir)
            for channel_dir in os.listdir(station_path):
                if not channel_dir.endswith('.D'):
                    continue
                channel_path = os.path.join(station_path, channel_dir)
                d_channel_path = os.path.join(d_station_path, channel_dir)
                ch_list = set()
                for mseed_file in os.listdir(channel_path):
                    seedid = '.'.join(mseed_file.split('.')[:4])
                    ch_list.add(seedid)
                for ch in list(ch_list):
                    net, sta, loc, cha = ch.split('.')
                    jday = BEGIN_DATE
                    t1 = datetime.strptime(BEGIN_DATE, '%Y.%j')
                    t2 = datetime.strptime(END_DATE, '%Y.%j')
                    delta = timedelta(days=1)
                    while t1 <= t2:
                        r_t2 = t1 + delta
                        mseed_file = '%s.D.%s' % (ch, t1.strftime('%Y.%j'))
                        d_mseed = os.path.join(d_channel_path, mseed_file)
                        try:
                            req = ('%s?network=%s&station=%s&location=%s&channel=%s&starttime=%s&endtime=%s' %
                                   (IRIS, net, sta, loc, cha, t1.strftime('%Y-%m-%d'), r_t2.strftime('%Y-%m-%d')))
                            print(req)
                            st = urlopen(req).read()
                            if not os.path.exists(d_year_path):
                                os.mkdir(d_year_path)
                            if not os.path.exists(d_network_path):
                                os.mkdir(d_network_path)
                            if not os.path.exists(d_station_path):
                                os.mkdir(d_station_path)
                            if not os.path.exists(d_channel_path):
                                os.mkdir(d_channel_path)
                            with open(d_mseed, 'w') as f:
                                print('write file %s' % d_mseed)
                                f.write(st)
                        except Exception as exception:
                            print('Error while retrieving data %s: %s' % (mseed_file, str(exception)))
                        t1 += delta


if __name__ == '__main__':
    main()
