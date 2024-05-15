# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil
import configparser
import sys
from obspy import read
from pathlib import Path
from utils.file_manager import load_json, scan_dir, write_json, create_dir
from obspy.core.stream import Stream


class SdsFiller(object):
    def __init__(self, config_file_path: str, station="*", output="./sds_filler_results", verbose=1) -> None:
        """Initialize class

        Args:
            config_file_path (str): Set path of config file
            src_source_sds (str): Set path of sds source
        """
        self.verbose = verbose
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)
        self.main_sds_path = self.config.get("sds", "path")
        self.src_source_sds = self.config.get("src", "path")
        self.report_path = output
        self.save_merged_file_path = self.config.get("merge", "path")
        self.files_in_source_sds = self._load_report("files_in_source_sds")             # ALL FILES IN SDS SRC
        self.files_already_in_main_sds = self._load_report("files_already_in_main_sds")   # FILES ALREADY IN MAIN SDS
        self.files_not_in_main_sds = self._load_report("files_not_in_main_sds")           # FILES NOT IN MAIN SDS
        self.files_in_both_with_diff = self._load_report("files_in_both_with_diff")       # FILES IN BOTH SDS WITH DIFF
        self.files_copied = self._load_report("files_copied")                             # FILES COPIED IN MAIN SDS
        self.files_merged = self._load_report("files_merged")                             # FILES MERGED IN MAIN SDS
        self.files_merged_failed = self._load_report("files_merged_failed")               # MERGED FILES THAT FAILED
        self.station = station

    def _search_file_in_main_sds(self, file_path: str):
        """
        This function takes a file from source SDS and
        search if this file exist in the main SDS

        Args:
            file_path (str): Set the file to search

        Returns:
            [bool] : return True if file exists
            [dict] : return dict with stat file in main SDS
        """
        pth = Path(file_path)

        if os.path.exists(pth):
            st_sds = os.stat(pth)
            dict_file = {'name': pth.name,
                         'abs_path': str(pth.absolute()),
                         'size': st_sds.st_size,
                         'last_m': st_sds.st_mtime,
                         'exist': True}
            return True, dict_file
        else:
          return False, {}


    def _compare_size(self, st_src: dict, st_sds: dict) -> bool:
        """Commpare size of 2 mseed file

        Args:
            st_src (dict): Set stat description of src file
            st_sds (dict): Set stat description of main sds file

        Returns:
            [bool]: return True if same size
        """
        if st_src['size'] == st_sds['size']: # SAME FILE
            return True
        else: # SAME NAME , SIZE IS DIFFERENT
            return False


    def _load_report(self, name: str) -> list:
        """Load report]

        Args:
            name (str): Set name of report

        Returns:
            list: [description]
        """
        path = os.path.join(self.report_path, '%s.json' % name) ## FIXME pb with
        if os.path.isfile(path):
            return load_json(path)
        else:
            return None

    def _write_report(self, name: str) -> None:
        """write report]

        Args:
            name (str): Set name of report

        """
        report_path = os.path.join(self.report_path, '%s.json' % name)
        if name == "files_in_source_sds":
            write_json(self.files_in_source_sds, report_path)
        elif name == "files_already_in_main_sds":
            write_json(self.files_already_in_main_sds, report_path)
        elif name == "files_not_in_main_sds":
            write_json(self.files_not_in_main_sds, report_path)
        elif name == "files_in_both_with_diff":
            write_json(self.files_in_both_with_diff, report_path)
        elif name == "files_copied":
            write_json(self.files_copied, report_path)
        elif name == "files_merged":
            write_json(self.files_merged, report_path)
        elif name == "files_merged_failed":
            write_json(self.files_merged_failed, report_path)
        else:
            print("Name %s not exist" % name)



    def _check_in_sds(self) -> None:
        """
        To check if the source file is present in the sds

        """
        self.files_not_in_main_sds = []
        self.files_already_in_main_sds = []
        self.files_in_both_with_diff = []
        for file_name in self.files_in_source_sds.keys():
            stat = self.files_in_source_sds[file_name]
            exist, st_sds = self._search_file_in_main_sds(
                self._get_file_path_in_main_sds(stat))
            if exist:
                if self._compare_size(stat, st_sds):
                    stat['comment'] = 'Size file: %s , Size file in SDS: %s' % (
                        stat['size'], st_sds['size'])
                    self.files_already_in_main_sds.append(stat) # Already in sds
                else:
                    stat['comment'] = 'Size file: %s , Size file in SDS: %s' % (
                        stat['size'], st_sds['size'])
                    self.files_in_both_with_diff.append(stat)  # Already in sds with size diff
            else:
                stat['comment'] = 'Not exit in SDS'
                self.files_not_in_main_sds.append(stat)  # not in sds

    def _get_file_path_in_main_sds(self, stat: dict) -> str:
        """To get path in SDS structure with stat description

        Args:
            stat (dict): Set stat description


        Returns:
            str: return path of file
        """
        files_sds_path = os.path.join(self.main_sds_path,
                                     stat['info']['year'],
                                     stat['info']['network'],
                                     stat['info']['station'],
                                     "%s.%s" % (stat['info']['channel'], stat['info']['quality']),
                                     stat["name"]
                                    )
        return files_sds_path

    def scan_source_sds(self) -> None:
        """
        Scan and list file in source sds
        """
        if self.verbose > 0:
            print('Scan dir: %s' % self.src_source_sds)
        self.files_in_source_sds = scan_dir(self.src_source_sds, sta = self.station)
        self._write_report("files_in_source_sds")
        if self.verbose > 0:
            print('%s files scanned' % len(self.files_in_source_sds))

    def get_diff_between_sds(self) -> None:
        """[summary]
        """
        if not os.path.exists(self.report_path):
            print("Error: dir does not exist  (Check output dir or Run --scan before --diff)")
            sys.exit(1)
        if self.verbose > 0:
            print('Search diff with the main SDS')
        self._check_in_sds()
        self._write_report("files_not_in_main_sds")
        self._write_report("files_already_in_main_sds")
        self._write_report("files_in_both_with_diff")

    def copy_list_file_in_sds(self) -> None:
        """
        To copy list file in sds
        """
        self.files_copied = []
        for st_file in self.files_not_in_main_sds:
            try:
                dist_path = self._get_file_path_in_main_sds(st_file)
                if not os.path.exists(dist_path):
                    if self.verbose > 1: 
                        print("Create rep : %s" % dist_path[:-len(st_file['name'])])
                    create_dir(dist_path[:-len(st_file['name'])])
                    shutil.copy(st_file['abs_path'], dist_path)
                    self.files_copied.append(st_file)
                    if self.verbose > 0:
                        print("File: %s copied" % st_file['name'])
                else :
                    print("The file %s already exist: Copy canceled " % dist_path)
            except:
                print("Error during copy : %s" % st_file['name']) 
        self._write_report("files_copied")

    def merge_file_in_both_sds(self) -> None:
        """
        To merge when there are mseed file in both sds

        """
        print("Merging starting")
        self.files_merged = []
        self.files_merged_failed = []
        for st_file in self.files_in_both_with_diff:
            try:
                st = Stream()
                overlap = False
                dist_path = self._get_file_path_in_main_sds(st_file)
                mseed_src = read(st_file['abs_path'])
                mseed_sds = read(dist_path)
                st += mseed_src
                st += mseed_sds
                st.merge(-1)
                gaps = st.get_gaps(min_gap=1)
                print("%s len = %s" % (st_file["name"], len(st)))
                for gap in gaps:
                    if gap[6] < 0:
                        overlap = True
                        break
                if not overlap:
                    print("Merge success")
                    save_path = os.path.join(self.save_merged_file_path, st_file['name'])
                    shutil.move(dist_path, save_path)
                    st_file['merge'] = {'old_file': save_path,
                                        'merge_time': str(datetime.utcnow()),
                                        'after':{'gap': str(gaps),
                                                 'start': str(st[0].stats['starttime']),
                                                 'end': str(st[0].stats['endtime'])},
                                        'before': {'gap_src': str(mseed_src.get_gaps(min_gap=1)),
                                                   'start_src': str(mseed_src[0].stats['starttime']),
                                                   'end_src': str(mseed_src[0].stats['endtime']),
                                                   'gap_sds': str(mseed_sds.get_gaps(min_gap=1)),
                                                   'start_sds': str(mseed_sds[0].stats['starttime']),
                                                   'end_sds': str(mseed_sds[0].stats['endtime'])}}
                
                    if not os.path.exists(dist_path):
                        st.write(dist_path, format="MSEED", reclen=512)
                        self.files_merged.append(st_file)
                    else:
                        st_file['merge_fail'] = {'fail_comment': 'file already exist'}
                        self.files_merged_failed.append(st_file)
                else:
                    print("Merge failled")
                    st_file['merge_fail'] = {'fail_time': str(datetime.utcnow()),
                                         #    'before': {'src': str(mseed_src.get_gaps()),
                                         #              'start_src': str(mseed_src[0].stats['starttime']),
                                         #               'end_src': str(mseed_sds[0].stats['starttime']),
                                         #               'sds': str(mseed_sds.get_gaps()),
                                         #               'start_sds': str(mseed_sds[0].stats['starttime']),
                                         #               'end_sds': str(mseed_sds[0].stats['endtime'])
                                         #               },
                                             'len_after_merge' : len(st)}
                    self.files_merged_failed.append(st_file)
            except:
                print("Error during merge : %s" % st_file['name'])
            print("Merge finished")
            self._write_report("files_merged")
            self._write_report("files_merged_failed")

    def get_reports(self) -> dict:
        """To get report

        Returns:
            dict: return all report
        """
        report = {
            "files_in_source_sds": self.files_in_source_sds,             # ALL FILES IN SDS SRC
            "files_already_in_main_sds": self.files_already_in_main_sds,   # FILES ALREADY IN MAIN SDS
            "files_not_in_main_sds": self.files_not_in_main_sds,           # FILES NOT IN MAIN SDS
            "files_in_both_with_diff": self.files_in_both_with_diff,       # FILES IN BOTH SDS WITH DIFF
            "files_copied": self.files_copied,                             # FILES COPIED IN MAIN SDS
            "files_merged": self.files_merged,                             # FILES MERGED IN MAIN SDS
            "files_merged_failed": self.files_merged_failed              # MERGED FILES THAT FAILED
        }
        return report

