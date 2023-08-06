#!/usr/bin/env python3
"""Functions to track writing progress."""
import os
import os.path
import datetime
from pathlib import Path
from src.trak.afile import File
from src.trak.session import Session

projects_path = Path(__file__).parent / "../data/projects.dat"
trackdata_path = Path(__file__).parent / "../data/trackdata.dat"
sessions_path = Path(__file__).parent / "../data/sessions.dat"
ignore_path = Path(__file__).parent / "../data/ignore.dat"
tmp_path = Path(__file__).parent / "../data/tmp.dat"


def write_trackdata():
    """Record the writing session in trackdata.dat"""
    # Read the tmp.dat file
    with open(tmp_path, 'r') as tmp:
        tmp_data = tmp.readlines()
        for i, line in enumerate(tmp_data):
            # Don't read the first line; it just contains the session ID
            # and start time.
            if i != 0:
                (s_id, p_name, f_path, s_wc) = line.strip().split(', ')
                this_file = File(p_name, f_path)
                f_wc = this_file.word_count()
                if f_wc - int(s_wc) != 0:
                    with open(trackdata_path, 'a') as t_d:
                        t_d.write(s_id + ', ' + p_name + ', ' +
                                  this_file.name() + ', ' +
                                  str(s_wc) + ', ' + str(f_wc) + '\n')


def n_words():
    """Return the total number of words tracked"""
    counter = 0
    with open(sessions_path, 'r') as f_data:
        s_data = f_data.readlines()
        for line in s_data:
            session_id = line.strip().split(', ')[0]
            session = Session(session_id)
            counter += session.total_wc()
    return counter


def n_sessions():
    """Return the total number of sessions tracked"""
    with open(sessions_path, 'r') as f_data:
        return len(f_data.readlines())


def n_files():
    """Return the total number of modified files"""
    u_projects = []
    u_files_list = []

    # Read trackdata.dat and compile a list of unique projects
    with open(trackdata_path, 'r') as f_record:
        f_data = f_record.readlines()
        for line in f_data:
            t_data = line.strip().split(', ')
            p_name = t_data[1]
            u_projects.append(p_name)

        # First, we gathered project names from each record in trackdata.dat.
        # Then, we apply that list to set() which ensures unique entries
        u_proj_set = set(u_projects)

        # For each unique project, gather all the modified files
        for proj in u_proj_set:
            p_files = []

            # Requires reading every line of trackdata.dat again
            for line in f_data:
                t_data = line.strip().split(', ')
                p_name = t_data[1]
                f_name = t_data[2]

                # If the project name matches the unique project name, add the
                # modified file to a list
                if p_name == proj:
                    p_files.append(f_name)

            # Only store unique modified files for this project
            u_files_set = set(p_files)

            # Convert the unique file set (for this project) to a list
            file_list = list(u_files_set)

            # Append this list to the unique files list (which ignores which
            # project these files came from). This establishes a 2D array
            # e.g., [[unique files for projA], [unique files for projB], ...]
            u_files_list.append(file_list)

    # Flatten the list, and count the elements. That count represents all the
    # unique files that have been modified in the tracked-data dataset.
    flattened_list = [y for x in u_files_list for y in x]
    return len(flattened_list)


def longest_session():
    """Return the longest recorded writing session"""
    session_list = []
    duration_list = []
    duration_dict = {}
    with open(sessions_path, 'r') as s_records:
        s_data = s_records.readlines()
        for line in s_data:
            session_id = line.strip().split(', ')[0]
            session = Session(session_id)
            duration = session.total_duration()
            session_list.append(session_id)
            duration_list.append(duration)
        for key, val in zip(session_list, duration_list):
            duration_dict[key] = val
        m_dur = max(duration_dict, key=duration_dict.get)
    return m_dur


def most_words():
    """Return the session where most words were written"""
    session_dict = {}
    with open(trackdata_path, 'r') as t_d:
        t_data = t_d.readlines()
        for line in t_data:
            t_ses = line.strip().split(', ')
            session_id = t_ses[0]
            session = Session(session_id)
            word_count = session.total_wc()
            session_dict[session_id] = word_count
    max_words = max(session_dict, key=session_dict.get)
    return max_words


def longest_streak():
    """Return a message regarding the date and length of longest writing streak"""
    tmp_lst = []
    streak_list = []
    with open(sessions_path, 'r') as s_s:
        s_data = s_s.readlines()
        for line in s_data:
            session_id = line.strip().split(', ')[0]
            session = Session(session_id)
            s_start = session.start_time()
            tmp_lst.append(s_start)
            length = len(tmp_lst)
            if length > 1:
                diff = tmp_lst[length - 1].date() - tmp_lst[length - 2].date()
                if diff.days != 1 and diff.days == 0:
                    del tmp_lst[-1]
                elif diff.days > 1:
                    del tmp_lst[-1]
                    streak_list.append(tmp_lst)
                    tmp_lst = [s_start]
        streak_list.append(tmp_lst)
        max_list = max(x for x in streak_list)
        start_streak_date = max_list[0].date()
        max_length = max(len(x) for x in streak_list)
        msg = "Starting on {}: {} days".format(start_streak_date, max_length)
    return msg


def current_streak():
    """Return the number of days in the current writing streak"""
    time_list = []
    streak_list = []
    streak = 0
    today = datetime.datetime.now()
    today = today.replace(microsecond=0)

    if os.stat(sessions_path).st_size != 0:

        # Create a list of start times to be used to determine current streak
        with open(sessions_path, 'r') as s_s:
            s_data = s_s.readlines()
            for line in s_data:
                s_time = line.strip().split(', ')[1]
                s_time = datetime.datetime.strptime(s_time, '%Y-%m-%d %H:%M:%S')
                time_list.append(s_time)
        diff = today - time_list[len(time_list) - 1]

        # streak is set to zero by default. Only do these calculations if sessions
        # have occurred on consecutive days
        if diff.days <= 1:

            # Before looping through start dates, add today to the streak list
            streak_list.append(today)

            # Loop through the start-time list in reverse; the last item in the
            # list is closest to today (newest records last)
            for time in reversed(time_list):
                streak_list.append(time)
                t_one = streak_list[len(streak_list) - 2]
                t_two = streak_list[len(streak_list) - 1]
                diff = t_one - t_two

                # Don't add to streak list if multiple sessions occurred in one day
                if diff.days == 0:
                    del streak_list[-1]

                # If difference is > 1, it's not longer a streak. Remove the last
                # entry (time)
                elif diff.days > 1:
                    del streak_list[-1]
                    break

            # The number of items in streak_list is the length of the current
            # streak
            streak = len(streak_list)
    return streak
