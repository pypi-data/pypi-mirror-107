#!/usr/bin/env python3
# -*- mode: python ; coding: utf-8 -*-
"""Tracks and analyses writing progress"""
import argparse
import datetime
import os.path
import sys
import uuid
from pathlib import Path

from tabulate import tabulate
from src.trak import core_methods
from src.trak.project import Project
from src.trak.session import Session
#from project import Project
#from session import Session

projects_path = Path(__file__).parent / "data/projects.dat"
trackdata_path = Path(__file__).parent / "data/trackdata.dat"
sessions_path = Path(__file__).parent / "data/sessions.dat"
ignore_path = Path(__file__).parent / "data/ignore.dat"
tmp_path = Path(__file__).parent / "data/tmp.dat"

def checks(trackstatus):
    tracking = trackstatus
    # The tmp.dat file is used to determine if tracking is on or off
    # If it exists, tracking is set to 'off'; otherwise it is 'on'.
    if not os.path.exists(tmp_path):
        tmp = open(tmp_path, 'w+')
        tracking = True
        uid = uuid.uuid1()
        new_session = Session(uid)
        tmp.close()

        # Test to make sure there's something to track
        number_of_projects = len(open(projects_path).readlines())
        if number_of_projects == 0:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print("Nothing to track! Use the -n option to track a project.")
            sys.exit()

    # If TRACKING == True, record initial data to a temporary file;
    # otherwise, record the tracking session to tracking.dat
    if tracking:
        # Write session info and start time at the top of tmp.dat
        new_session.timestamp_tmp()

        # Store tracked files & initial word counts in tmp.dat
        new_session.write_tmp()

        # Display a message indicating that tracking has begun
        print(new_session.start_msg())

    else:
        # Retrieve the session ID from the top of tmp.dat
        with open(tmp_path, 'r') as tmp:
            dat = tmp.readline()
            session_ID = dat.strip().split(', ')[0]

        # Create a new session object
        old_session = Session(session_ID)

        # Write session data to trackdata.dat
        core_methods.write_trackdata()

        # Write the session details to file
        old_session.write_session()

        # Display a closing message
        print(old_session.end_msg)

    # TRACKING is False at the beginning of the program by default.
    # It's only made True when tmp.dat is created and the user wants to
    # track something. So, when tracking is False, it means that
    # tmp.dat already exists, which only happens when the user has run
    # 'trak' already. It was never made True at the initiation of this
    # instance of the program. If so, delete tmp.dat. The data have already
    # been recorded.
    if not tracking:
        os.remove(tmp_path)
        
    # return tracking

def main():


    # Create files where data will be stored if they don't exist already
    if not os.path.exists(projects_path):
        projects = open(projects_path, 'a')

    if not os.path.exists(trackdata_path):
        trackdata = open(trackdata_path, 'a')

    if not os.path.exists(sessions_path):
        sessions = open(sessions_path, 'a')

    if not os.path.exists(ignore_path):
        ignore = open(ignore_path, 'a')

    # Parse program options
    parser = argparse.ArgumentParser(description="Track and analyse writing progress")
    parser.add_argument("-d", "--delete",
                        help="remove file or project from further tracking; remove ignored file to resume tracking")

    parser.add_argument("-e", "--export",
                        help="export data to stdout")

    parser.add_argument("-l", "--list",
                        help="list ignores, files, sessions, or projects")

    parser.add_argument("-n", "--new",
                        help="track a new writing project",
                        action="store_true")

    parser.add_argument("-r", "--record",
                        help="display all-time tracking records",
                        action="store_true")

    parser.add_argument("-s", "--summary",
                        help="display summary of selected session",
                        action="store_true")

    parser.add_argument("-x", "--expunge",
                        help="delete all data; restore factory defaults",
                        action='store_true')

    parser.add_argument("-z", "--status",
                        help="determine whether tracking is on or off",
                        action='store_true')

    args = parser.parse_args()

    #####################################################
    #           Process user options                  ##
    #####################################################
    if args.expunge:
        MSG = "This option will remove all data and return to factory defaults." + \
              "\n" + "WARNING: This cannot be undone.\n"
        print(MSG)

        response = input('Are you sure you want to proceed with reset (y/n): ')
        if response == 'y':
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            os.remove(ignore_path)
            os.remove(projects_path)
            os.remove(sessions_path)
            os.remove(trackdata_path)
            print('Tracking has been restored to factory defaults')
        else:
            print('Action cancelled by user. Nothing removed.')

        sys.exit()

    if args.export:
        if args.export == 'tracks':
            with open(trackdata_path, 'r') as f:
                t_data = f.readlines()
                print('track_id, project_name, file_name, start_wc, end_wc')
                for line in t_data:
                    print(line.strip())

        elif args.export == 'files':
            with open(projects_path, 'r') as f:
                p_data = f.readlines()
                for line in p_data:
                    (p_name, p_path) = line.strip().split(', ')
                    project = Project(p_name, p_path)
                    p_list = project.filepath_list()
                    for file in p_list:
                        print(file)

        elif args.export == 'projects':
            print('project_name, project_path')
            with open(projects_path, 'r') as f:
                p_data = f.readlines()
                for line in p_data:
                    print(line.strip())

        elif args.export == 'sessions':
            print('session_id, start_time, end_time')
            with open(sessions_path, 'r') as f:
                s_data = f.readlines()
                for session in s_data:
                    print(session.strip())

        else:
            print("Invalid entry. Valid entries include: tracks, files, projects, or sessions")
            sys.exit()
        sys.exit()

    if args.record:
        
        # Test to make sure there are data for which records can be estblished 
        number_of_tracks = len(open(trackdata_path).readlines())
        if number_of_tracks == 0:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print("No tracks have been recorded; no records can be displayed.")
            sys.exit()

        r_list = [['Total number of words tracked', core_methods.n_words()],
                  ['Total number of sessions tracked', core_methods.n_sessions()],
                  ['Total number of modified files', core_methods.n_files()]]
        l_session = Session(core_methods.longest_session())
        duration = l_session.total_duration()
        duration = duration - datetime.timedelta(microseconds=duration.microseconds)
        session_time = l_session.start_time()
        session_date = session_time.date()
        r_list.append(['Longest session', str(session_date) + " " + str(duration)])
        w_session = Session(core_methods.most_words())
        max_wc = w_session.total_wc()
        s_start = w_session.start_time()
        s_date = s_start.date()
        r_list.append(['Most words written in a session', str(s_date) + ' ' + str(max_wc) + ' words'])
        r_list.append(['Longest writing streak', core_methods.longest_streak()])
        r_list.append(['Current streak', '{} days'.format(core_methods.current_streak())])
        table = tabulate(r_list)
        print(table)

        sys.exit()

    if args.status:
        MSG = ''
        if os.path.exists(tmp_path):
            with open(tmp_path, 'r') as tmp:
                tmp_data = tmp.readline()
                s_id = tmp_data.strip().split(', ')[0]
                s_start = tmp_data.strip().split(', ')[1]
            MSG = 'Tracking is ON\n' + \
                  'This tracking session began at ' + s_start + '\n' + \
                  'Current writing streak is ' + str(core_methods.current_streak()) + ' days'
        else:
            MSG = 'Tracking is OFF\n' + \
                  'Current writing streak is ' + str(core_methods.current_streak()) + ' days'
        print(MSG)
        sys.exit()

    if args.summary:
        # Display a selection list of available sessions
        sessions_list = []
        with open(sessions_path, 'r') as s:
            if os.stat(sessions_path).st_size == 0:
                print('No writing sessions recorded. Process halted.')
                sys.exit()
            sessions_data = s.readlines()
            for i, line in enumerate(sessions_data):
                s_time = line.strip().split(', ')[1]
                e_time = line.strip().split(', ')[2]
                print('[' + str(i) + '] ' + s_time + ' to ' + e_time)
                sessions_list.append(line)

        # Get input from user
        try:
            selection = int(input('Select session to summarise [0-' +
                                  str(len(sessions_list) - 1) + ']: '))
        except ValueError:
            print('Invalid input. Integer expected.')
            sys.exit()
        while len(sessions_list) > 1 and selection not in range(len(sessions_list)):
            try:
                selection = int(input('Invalid input. Please select valid session [0-' +
                                      str(len(sessions_list) - 1) + ']: '))
            except ValueError:
                print('Invalid input. Integer expected')
                sys.exit()
        session_ID = sessions_list[selection].strip().split(', ')[0]
        session = Session(session_ID)
        print(session.summary())
        print('Modified Files')
        print(session.modified_files())
        sys.exit()

    if args.delete:
        if args.delete == 'file':
            # Get input from the user, and check it
            proj_name = input('Project in which file resides: ')
            project = Project(proj_name, )
            while not project.is_name_taken():
                print('No project is named {}: please try again'.format(proj_name))
                proj_name = input('Project in which file resides: ')
                if proj_name == "":
                    print('File deletion halted by user. Nothing deleted.')
                    sys.exit()
                project = Project(proj_name, )
            proj_path = project.get_path()

            # If proj_path is already a file, just add it to ignore.dat
            path_exp = os.path.expanduser(proj_path)
            if os.path.isfile(path_exp):
                with open('ignored_files.dat', 'a') as ignore:
                    ignore.write(proj_name + ', ' + str(proj_path) + '\n')
                    print('The file {} was successfully ignored'.format(proj_path))
                    sys.exit()

            # Present the user with a numbered list of candidate files to delete
            # from this project.
            project = Project(proj_name, proj_path)
            f_names = project.filepath_list()
            print('Files belonging to project {}'.format(proj_name))
            for i, file in enumerate(f_names):
                print('[' + str(i) + '] ' + file)
            try:
                f_select = int(input('Choose a file to ignore [0-' + str(len(f_names) - 1) + ']: '))
            except ValueError:
                print('Invalid selection. Expected an integer.')
                sys.exit()

            # Write the path to the ignore file, and it will no longer be tracked.
            path_select = f_names[f_select]
            with open(ignore_path, 'a') as ignored:
                ignored.write(proj_name + ', ' + path_select + '\n')
            print('The file {} will no longer be tracked'.format(path_select))

        elif args.delete == 'ignore':
            if os.stat(ignore_path) == 0:
                print('No files are currently being ignored. Nothing to display.')
                sys.exit()
            i_list = []
            max_i = 0
            with open(ignore_path, 'r') as iggy:
                i_data = iggy.readlines()
                for i, line in enumerate(i_data):
                    (project_name, file_path) = line.strip().split(', ')
                    i_list.append([project_name, file_path])
                    print('[' + str(i) + ']', project_name, file_path)
                if len(i_list) > 0:
                    max_i = len(i_list) - 1
                else:
                    print('No files are currently being ignored. Action halted.')
                    sys.exit()

                # Get input from user
                try:
                    selection = int(input('Select a file to stop ignoring [0-' + str(max_i) + ']: '))
                except ValueError:
                    print('Invalid input. Integer expected.')
                    sys.exit()
                while len(i_list) > 1 and selection not in range(len(i_list)):
                    try:
                        selection = int(
                            input('Invalid input. Please select valid ignore file [0-' + str(max_i) + ']: '))
                    except ValueError:
                        print('Invalid input. Integer expected')
                        sys.exit()
            sel_proj = i_list[selection][0]
            sel_file = i_list[selection][1]
            with open(ignore_path, 'w') as iggy:
                for item in i_list:
                    project_name = item[0]
                    file_path = item[1]
                    if not (project_name == sel_proj and file_path == sel_file):
                        iggy.write(project_name + ', ' + file_path + '\n')
            print('The file {} in project {} will now be tracked'.format(sel_file, sel_proj))

        elif args.delete == 'project':
            proj_name = input('Project name to stop tracking: ')
            with open(projects_path, 'r') as proj:
                lines = proj.readlines()
                project = Project(proj_name, )
                while not project.is_name_taken():
                    print('No project is named {}: please try again'.format(proj_name))
                    proj_name = input('Project name to stop tracking: ')
                    if proj_name == "":
                        print('File deletion halted by user. Nothing deleted.')
                        sys.exit()
            with open(projects_path, 'w') as proj:
                for line in lines:
                    (p_name, p_path) = line.strip('\n').split(', ')
                    if p_name != proj_name:
                        proj.write(p_name + ', ' + p_path + '\n')
            print('Project {} will no longer be tracked.'.format(proj_name))

        else:
            print("Acceptable arguments are: ignore, file, or project. Nothing removed")
        sys.exit()

    if args.list:
        if args.list == 'files':
            FILES = 0
            if os.stat(projects_path).st_size == 0:
                print("Nothing is currently being tracked. No files to display.")
            else:
                with open(projects_path, 'r') as proj:
                    p_data = proj.readlines()
                    for line in p_data:
                        (p_name, p_path) = line.strip().split(', ')
                        this_project = Project(p_name, p_path)
                        print('Project {}:\n'.format(p_name))
                        f_list = this_project.filepath_list()
                        FILES += len(f_list)
                        for file in f_list:
                            print(file)
                print('Total: {} files tracked'.format(FILES))
        elif args.list == 'ignores':
            i_list = []
            if os.stat(ignore_path).st_size == 0:
                print("No files are currently being ignored. Nothing to display.")
                sys.exit()
            else:
                with open(ignore_path) as iggy:
                    i_data = iggy.readlines()
                    for line in i_data:
                        i_list.append(line.strip().split(', '))
                table = tabulate(i_list, headers=['Project', 'Ignored Files'])
                print(table)
        elif args.list == 'sessions':
            s_list = []
            if os.stat(sessions_path).st_size == 0:
                print("No sessions have been recorded. Nothing to display.")
                sys.exit()
            else:
                with open(sessions_path, 'r') as ses:
                    s_data = ses.readlines()
                    for line in s_data:
                        s_list.append(line.strip().split(', '))
                table = tabulate(s_list, headers=['Session ID', 'Start time', 'End time'])
                print(table)
        elif args.list == 'projects':
            p_list = []
            if os.stat(projects_path).st_size == 0:
                print("No projects are currently being tracked. Nothing to display")
            else:
                with open(projects_path, 'r') as proj:
                    p_data = proj.readlines()
                    for line in p_data:
                        p_list.append(line.strip().split(', '))
                table = tabulate(p_list, headers=['Project name', 'Project path'])
                print(table)
        else:
            print("Acceptable arguments are: ignores, files, projects, sessions.")
        sys.exit()

    elif args.new:

        # User wants to add a new project
        project_name = input("Name of new project: ")

        with open(projects_path, 'r') as proj:
            p_data = proj.readlines()
            for line in p_data:
                this_line = line.strip().split(', ')
                if this_line[0] == project_name:
                    project_name = input("Name of new project: ")
                    if project_name == "":
                        print("New project tracking halted by user. Nothing tracked.")
                        sys.exit()

        # User inputs the path of the new project
        project_path = input("Path of new project: ")

        # Make sure that the given path actually exists
        while not os.path.exists(os.path.expanduser(project_path)):
            print('\nPath does not exist. Please try again.')
            project_path = input("Path of new project: ")
            if project_path == "":
                print("Tracking halted by user. Nothing tracked.")
                sys.exit()

        # Make sure that the path that was provided isn't already being tracked.
        with open(projects_path, 'r') as f:
            for line in f.readlines():
                (line_proj, line_path) = line.strip('\n').split(', ')

                if project_path == line_path:
                    print("\nThe path {} is already being tracked as {}".format(line_path, line_proj))
                    print("Nothing was added to the projects catalogue.")
                    sys.exit()

        # Once all the checks have passed, create a new project
        new_project = Project(project_name, project_path)

        # Display a message once project's been written to file
        print(new_project.write_project())

        # Exit once the new project has been recorded
        sys.exit()

    checks(False)


if __name__ == '__main__':
    sys.exit(main())

