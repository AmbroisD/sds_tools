import sys
import json
from utils.file_manager import load_json
from collections import Counter

def get_infos_with_name(name):
    list_infos = name.split('.')
    return list_infos[0], list_infos[1], list_infos[2], list_infos[3], list_infos[5], list_infos[6]


def main(json_file, year_f=None):
    data_list = load_json(json_file)
    print(len(data_list))
    year = []
    station = []
    network = [] 
    channel = []
       
    for x in data_list:
        name = x['name']
        net, sta, _, cha, y, d = get_infos_with_name(name)
        if y == year_f or year_f is None:
            year.append(y)
            station.append(sta)
            channel.append(cha)
            network.append(net)

    print("Nb file by year: %s" % Counter(year))
    print("Nb file by station: %s" % Counter(station))
    print("Nb file by channel: %s" % Counter(channel))
    print("Nb file by network: %s" % Counter(network))
     
    

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        main(sys.argv[1])  

