# -*- coding: utf-8 -*-
from utils.sdsfiller import SdsFiller


def get_general_resume(reports):
    len(reports["files_in_both_with_diff"])

def main(config, verbose):
    """
    Basic main function.

    -scan all files
    -create json for each station
    """

    my_sds_filler = SdsFiller(config, verbose)
    reports = my_sds_filler.get_reports()
    
    for st_file in reports["files_in_both_with_diff"]:
        

if __name__ == '__main__':
    main()
