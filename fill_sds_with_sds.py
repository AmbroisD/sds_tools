# -*- coding: utf-8 -*-
import argparse
from utils.sdsfiller import SdsFiller


def main():
    """
    Basic main function.

    -scan all files
    -create json for each station
    """
    parser = argparse.ArgumentParser(description="""sds filler
                                     Several steps:
                                     - First scan the files to import (--scan)
                                     - Then compare with the main sds (--diff)
                                     - Then filled with files not yet present (--fill)
                                     - Finally compare and replace the files if the files exist in both sds (--replace)
                                     or
                                     - Execute all steps automatically (--auto)
                                     """)

    parser.add_argument('-c', "--config", default="config.ini",
                        help='Set configuration file')
    parser.add_argument('-y', "--year", help='Set year')
    parser.add_argument('-p', '--program', default="file-analyse",
                        help='The path of file-analyze')
    parser.add_argument('-a', "--auto", action="store_true", default=False,
                        help='Fill sds in automatic')
    parser.add_argument('-s', "--scan", action="store_true", default=False,
                        help='Scan sds or directories')
    parser.add_argument('-d', "--diff", action="store_true", default=False,
                        help='Compare with file in main sds and search diff')
    parser.add_argument('-f', "--fill", action="store_true", default=False,
                        help='Fill main sds with files that are not yet present')
    parser.add_argument('-m', "--merge", action="store_true", default=False,
                        help='Compare the files between the sds and choose the file with the most data')
    parser.add_argument('-v', '--verbose', action='count', default=1)
    args = parser.parse_args()

    #config = load_config(args.config)

    my_sds_filler = SdsFiller(args.config,
                              verbose = args.verbose)
    if args.scan:  # TODO add auto
        my_sds_filler.scan_another_sds()
    if args.diff:  # TODO add auto
        my_sds_filler.get_diff_between_sds()
    if args.fill:  # TODO add auto
        my_sds_filler.copy_list_file_in_sds()
    if args.merge:  # TODO add auto
        my_sds_filler.merge_file_in_both_sds()


if __name__ == '__main__':
    main()
