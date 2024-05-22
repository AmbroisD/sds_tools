# -*- coding: utf-8 -*-
from datetime import datetime
import sys
import json
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
                                     - Finally compare and merge files if the files exist in both sds (--merge)
                                     """)

    parser.add_argument('-c', "--config", default="config.ini",
                        help='Set configuration file')
    parser.add_argument("-o", "--output", default="./results",
                        help='Set result dir')
    #parser.add_argument('-r', "--report", help='Print resume of report')
    parser.add_argument('--station', default="*",
                        help='filtering data based on a specific station')
    parser.add_argument('--location', default="*",
                        help='filtering data based on a specific location code')
    parser.add_argument('-y', '--year', default="*",
                        help='filtering data based on a specific year')
    parser.add_argument('--all', action='store_true', default=False,
                        help='Process all data')
    #parser.add_argument('-a', "--auto", action="store_true", default=False,
    #                    help='Fill sds in automatic')
    parser.add_argument('-s', "--scan", action="store_true", default=False,
                        help='Scan sds or directories')
    parser.add_argument('-d', "--diff", action="store_true", default=False,
                        help='Compare with file in main sds and search diff')
    parser.add_argument('-f', "--fill", action="store_true", default=False,
                        help='Fill main sds with files that are not yet present')
    parser.add_argument('-m', "--merge", action="store_true", default=False,
                        help='Compare the files between the sds and merge file data')
    parser.add_argument('-p', '--print_info', action='store_true', default=False,
                        help='Print the contents of the .info file')
    parser.add_argument('-v', '--verbose', action='count', default=1)
    args = parser.parse_args()

    #config = load_config(args.config)
    if args.print_info:
        with open(f"{args.output}/.info", "r") as f:
            execution_status = json.load(f)
    
        print("Execution Status:")
        for key, value in execution_status.items():
            print(f"[{key: <5}]: Completed: {str(value[0]):5s} | Date : {value[1]}")
        sys.exit(0)
    
        # Check that either --station or --all is provided, but not both
    if (args.station == "*" and not args.all) or (args.station != "*" and args.all):
        parser.error("You must specify either --station or --all, but not both.")

       # Read existing execution status file if present
    try:
        with open(f"{args.output}/.info", "r") as f:
            execution_status = json.load(f)
    except FileNotFoundError:
        execution_status = {"scan": [False, None], "diff": [False, None], "fill": [False, None], "merge": [False, None]}

    my_sds_filler = SdsFiller(args.config,
                              station = args.station,
                              location = args.location,
                              year = args.year,
                              output = args.output,
                              verbose = args.verbose
                              )
    
    if args.scan:
        my_sds_filler.scan_source_sds()
        execution_status["scan"] = [True, datetime.now().strftime("%Y-%m-%dT%H:%M:%S")]  # Update execution status

        # Handle existing files if --scan is used after previous runs
        if execution_status["diff"][0] or execution_status["fill"][0] or execution_status["merge"][0]:
            print("Warning: Previous execution results detected. Overwriting existing files.")
            execution_status["diff"] = [False, None]
            execution_status["fill"] = [False, None]
            execution_status["merge"] = [False, None]
    if args.diff:
        if not execution_status["scan"][0]:
            print("Error: --diff cannot be performed before --scan.")
        else:
            my_sds_filler.get_diff_between_sds()
            execution_status["diff"] = [True, datetime.now().strftime("%Y-%m-%dT%H:%M:%S")]  # Update execution status

    if args.fill:
        if not execution_status["diff"][0]:
            print("Error: --fill cannot be performed before --diff.")
        else:
            my_sds_filler.copy_list_file_in_sds()
            execution_status["fill"] = [True, datetime.now().strftime("%Y-%m-%dT%H:%M:%S")]  # Update execution status

    if args.merge:
        if not execution_status["diff"][0]:
            print("Error: --merge cannot be performed before --scan and --diff.")
        else:
            my_sds_filler.merge_file_in_both_sds()
            execution_status["merge"] = [True, datetime.now().strftime("%Y-%m-%dT%H:%M:%S")]  # Update execution status

    # Write execution status to output file
    with open(f"{args.output}/.info", "w") as f:
        json.dump(execution_status, f, indent=4)

    # Print .info file contents if requested

    #if args.scan:  # TODO add auto
    #    my_sds_filler.scan_source_sds()
    #if args.diff:  # TODO add auto
    #    my_sds_filler.get_diff_between_sds()
    #if args.fill:  # TODO add auto
    #    my_sds_filler.copy_list_file_in_sds()
    #if args.merge:  # TODO add auto
    #    my_sds_filler.merge_file_in_both_sds()


if __name__ == '__main__':
    main()
