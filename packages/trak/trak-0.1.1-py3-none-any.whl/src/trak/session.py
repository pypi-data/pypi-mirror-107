#!/usr/bin/env python3
"""Functions to track writing progress."""
import datetime
import os
import os.path
from pathlib import Path

from src.trak.project import Project
from tabulate import tabulate

from src.trak.afile import File

projects_path = Path(__file__).parent / "../data/projects.dat"
tracked_data_path = Path(__file__).parent / "../data/trackdata.dat"
sessions_path = Path(__file__).parent / "../data/sessions.dat"
ignore_path = Path(__file__).parent / "../data/ignore.dat"
tmp_path = Path(__file__).parent / "../data/tmp.dat"


class Session:
    """A track-writing session"""

    def __init__(self, uid):
        self.session_id = uid
        self.current_time = datetime.datetime.now().replace(microsecond=0)

    def timestamp_tmp(self):
        """Write session ID and start time to tmp.dat file"""
        with open(tmp_path, 'a') as tmp:
            tmp.write(str(self.session_id) + ', ' + str(self.current_time) + '\n')

    def write_tmp(self):
        """Write tmp.dat with every tracked file and starting word count"""
        with open(projects_path, 'r') as proj:
            projects = proj.readlines()
            for line in projects:
                (p_name, p_path) = line.strip().split(', ')
                this_project = Project(p_name, p_path)
                for file in this_project.filepath_list():
                    # f_path = "~/" + file
                    this_file = File(p_name, file)
                    this_wc = this_file.word_count()
                    with open(tmp_path, 'a') as tmp:
                        tmp.write(str(self.session_id) + ', ' + this_project.p_name + ', ' +
                                  file + ', ' + str(this_wc) + '\n')

    def write_session(self):
        """Write session details to sessions.dat"""

        # ID and start time are stored in the top line of tmp.dat
        with open(tmp_path, 'r') as tmp:
            s_info = tmp.readline()
            s_start = s_info.strip().split(', ')[1]
            s_end = self.current_time

        # If sessions.dat is empty, just record the data
        if os.stat(sessions_path).st_size == 0 and self.total_wc() != 0:
            with open(sessions_path, 'a') as f_empty:
                f_empty.write(str(self.session_id) + ', ' + s_start + ', ' + str(s_end) + '\n')

        # If the session has already been recorded, don't write anything
        with open(sessions_path, 'r') as f_read:
            line_data = f_read.readlines()
            if any(line.strip().split(', ')[0] == self.session_id for line in line_data):
                return

        # If the session has not been recorded, write the session data to file
        if self.total_wc() != 0:
            with open(sessions_path, 'a') as f_write:
                f_write.write(self.session_id + ', ' + str(s_start) + ', ' + str(s_end) + '\n')

    def start_time(self):
        """Return the tracking start time"""
        # The start time can exist in two places:
        # 1. The first line of tmp.dat if the session just started
        # 2. The sessions.dat file if the session has already been recorded
        # s_start = datetime.datetime
        with open(sessions_path, 'r') as tmp:
            s_data = tmp.readlines()
            for line in s_data:
                s_id = line.strip().split(', ')[0]
                if s_id == self.session_id:
                    start_str = line.strip().split(', ')[1]
                    s_start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                    break
            else:
                with open(tmp_path, 'r') as t_data:
                    s_data = t_data.readline()
                    start_str = s_data.strip().split(', ')[1]
                    s_start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
            s_start = s_start.replace(microsecond=0)
        return s_start

    def end_time(self):
        """Return the tracking end time"""
        # The only place where the end time is stored is in sessions.dat
        s_end = datetime.datetime
        with open(sessions_path, 'r') as tmp:
            s_data = tmp.readlines()
            for line in s_data:
                s_id = line.strip('\n').split(', ')[0]
                end_str = line.strip('\n').split(', ')[2]
                s_end = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
                if s_id == self.session_id:
                    break
        s_end = s_end.replace(microsecond=0)
        return s_end

    def start_msg(self):
        """Return a message appropriate for the start of a tracking session"""
        files_tracked = 0
        with open(projects_path, 'r') as proj:
            p_data = proj.readlines()
            for line in p_data:
                (p_name, p_path) = line.strip().split(', ')
                this_project = Project(p_name, p_path)
                files_tracked += this_project.n_tracked()
        start_msg = 'Tracking started at ' + str(self.start_time()) + '\n' + \
                    'Number of files tracked: ' + str(files_tracked)
        return start_msg

    def total_wc(self):
        """Return the total number of words written during this session"""
        # Total number of words written
        t_wc = 0
        with open(tracked_data_path, 'r') as t_d:
            s_data = t_d.readlines()
            for line in s_data:
                t_line = line.strip().split(', ')
                s_id = t_line[0]
                s_wc = t_line[3]
                f_wc = t_line[4]
                if s_id == str(self.session_id):
                    t_wc += int(f_wc) - int(s_wc)
        return t_wc

    def total_duration(self):
        """Return the total duration of the writing session"""
        duration = self.end_time() - self.start_time()
        return duration

    def n_modified(self):
        """Return the number of modified files in the writing session"""
        num_files = 0
        with open(tracked_data_path, 'r') as t_d:
            dat = t_d.readlines()
            for line in dat:
                s_id = line.strip().split(', ')[0]
                if s_id == self.session_id:
                    num_files += 1
        return num_files

    def modified_files(self):
        """Return a list of files modified during writing session"""
        file_list = []
        with open(tracked_data_path, 'r') as t_d:
            dat = t_d.readlines()
            for line in dat:
                (s_id, p_name, file_name, wc_start, wc_end) = line.strip().split(', ')
                # s_id = line.strip().split(', ')[0]
                # file_name = line.strip().split(', ')[2]
                # wc_start = line.strip().split(', ')[3]
                # wc_end = line.strip().split(', ')[4]
                wc_fin = int(wc_end) - int(wc_start)
                if s_id == self.session_id:
                    file_list.append([p_name, file_name, wc_fin])
        msg = tabulate(file_list, headers=['Project', 'File', 'Words Written'])
        return msg

    def summary(self):
        """Return a summary of a writing session"""
        table = [['Session ID', self.session_id],
                 ['Start time', self.start_time()],
                 ['End time', self.end_time()],
                 ['Total duration', self.total_duration()],
                 ['Files modified', self.n_modified()],
                 ['Total word count', self.total_wc()]]
        msg = tabulate(table)
        return msg

    @property
    def end_msg(self):
        """Return a message appropriate for the end of a tracking session"""
        was_were = ' file was' if self.n_modified() == 1 else ' files were'
        if self.total_wc() == 0:
            msg = "Tracking ended at " + str(self.current_time) + '\n' + \
                  "No tracked files were modified. Session not recorded."
        else:
            msg = "Tracking ended at " + str(self.current_time) + '\n' + \
                  str(self.n_modified()) + was_were + " modified for a total of " + \
                  str(self.total_wc()) + " words written." + '\n' + \
                  "Total writing duration was " + str(self.total_duration())
        return msg
