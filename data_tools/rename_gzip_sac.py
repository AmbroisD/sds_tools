import io
import os
import sys
import obspy
import shutil
import tarfile
import pathlib
import tempfile
from pathlib import Path
from os.path import relpath


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.join(SCRIPT_DIR, '..', 'utils')))
from utils.file_manager import load_json, check_dates_window

MAXDATES = "2022-09-01"
rename_tar_result = "./result" 
rep_gzip = "../../data/sac_gzip/"

#s2rhai2021pwii/s2rhai2021pwii.tar.gz"

def test_network_in_tar_file(targz_file, net="AM"):
    t = tarfile.open(targz_file, 'r:gz')
    for finfo in t.getmembers():
        if finfo.name.split("_")[0] == net:
            return True
    return False


def get_config(cfg_file):
    """Extract infos in cfg file

    :param cfg_file: Set the config file
    :type cfg_file: str
    """
    return load_json(cfg_file)


def scan_dir(dir):
    file_in_dir = {}
    for path in Path(dir).rglob('*/*.tar.gz'):
        st = os.stat(path.absolute())
        file_in_dir[path.name] = {'name': path.name,
                                  'abs_path': str(path.absolute()),
                                  'path_in_sds': relpath(str(path.absolute()), dir),
                                  'size': st.st_size,
                                  'last_m': st.st_mtime}
    return file_in_dir


def rename_data(tr, station=None, network=None, location=None, channel=None):
    """
    To rename trace

    :param tr: Set Trace to rename
    :type tr: obspy.trace
    :param station: Set new station name, defaults to None
    :type station: str, optional
    :param network: Set new network name, defaults to None
    :type network: str, optional
    :param location: Set new location name, defaults to None
    :type location: str, optional
    :param channel: Set new channel name, defaults to None
    :type channel: str, optional
    :return: return the new trace
    :rtype: obspy.trace
    """
    if station is not None:
        tr.stats.station = station
    if network is not None:
        tr.stats.network = network
    if location is not None:
        tr.stats.location = location
    if channel is not None:
        tr.stats.channel = channel
    return tr


def get_new_name(info, list_conf, year_jday):
    for current_conf in list_conf:
        date = current_conf["date"]
        if current_conf['old'][0] == info[0] and current_conf['old'][1] == info[1]:
            if check_dates_window(f"{year_jday}", date['start'], date['end'], max_date=MAXDATES):
                return True, current_conf['new'], f"{current_conf['new'][0]}_{current_conf['new'][1]}_{info[2]}_{info[3]}"
    return False, None, None


def main(config, net="AM"):
    list_conf = get_config(config)
    list_in_dir = scan_dir(os.path.join(rep_gzip))
    for key, values in list_in_dir.items():
        if test_network_in_tar_file(values['abs_path'],  net=net):    
            """Extract archive to temporary directory, replace file, replace archive """
            # tempdir
            with tempfile.TemporaryDirectory() as td:
                # dirname to Path
                tdp = pathlib.Path(td)
        
                # extract archive to temporry directory
                with tarfile.open(values['abs_path']) as r:
                    for finfo in r.getmembers():
                        info = finfo.name.split("_")
                        print(info)
                        if info[0] != net:
                            r.extract(finfo, td)
                        else:
                            fileobj = r.extractfile(finfo)
                            st = obspy.read(fileobj)
                            year_jday = st[0].stats.starttime.strftime("%Y.%j")
                            bool_new, new, new_name= get_new_name(info, list_conf, year_jday)
                            if bool_new:
                                for tr in st:
                                    rename_data(tr, station=new[1], network=new[0])
                            else:
                                new_name = finfo.name
                                print(f"no new name for {info[1]}")
                            st.write(os.path.join(tdp, new_name), format='SAC')
                # replace archive, from all files in tempdir
                with tarfile.open(os.path.join(rename_tar_result, values['name']), "w:gz") as w:
                    for f in tdp.iterdir():
                        w.add(f, arcname=f.name)
        else:
            shutil.copy(values['abs_path'], os.path.join(rename_tar_result, values['name']))
                

if __name__ == "__main__":
    main("./config/haiti_RS.json")
    #add_file(rep_gzip, "./tmp.sac")