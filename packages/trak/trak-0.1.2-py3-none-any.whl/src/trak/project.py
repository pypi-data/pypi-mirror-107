#!/usr/bin/env python3
"""Functions to track writing progress."""
import os
import os.path
from pathlib import Path

projects_path = Path(__file__).parent / "../data/projects.dat"
ignore_path = Path(__file__).parent / "../data/ignore.dat"


class Project:
    """A writing project"""

    def __init__(self, project_name, path=''):
        self.p_name = project_name
        self.path = path

    def is_file(self):
        """Return True if URL is a file"""
        return os.path.isfile(os.path.expanduser(self.path))

    def is_name_taken(self):
        """Return True if project name is already in use"""
        with open(projects_path, "r") as proj:
            return any(line.strip('\n').split(', ')[0] == self.p_name for line in proj)

    def get_path(self) -> object:
        """Return a path for a named project"""
        with open(projects_path, 'r') as proj:
            proj_list = proj.readlines()
            for line in proj_list:
                (p_name, p_path) = line.strip().split(', ')
                if p_name == self.p_name:
                    break
        return p_path

    def get_ignored(self):
        """Return a list of ignored files"""
        i_files = []
        with open(ignore_path, 'r') as ignored:
            lines = ignored.readlines()
            for line in lines:
                (proj, path) = line.strip().split(', ')
                if proj == self.p_name:
                    i_files.append(path)
        return i_files

    def filepath_list(self):
        """Return a list of all the .txt and .tex files in a project"""
        expanded_path = os.path.expanduser(self.path)
        f_list = []
        if os.path.isfile(expanded_path):
            f_list = [self.path]
        elif os.path.isdir(expanded_path):
            for root, dirs, files in os.walk(expanded_path):
                for name in files:
                    if name.endswith('.txt') or name.endswith('.tex') \
                            or name.endswith('.md') or name.endswith('.html'):
                        n_path = root.replace(os.path.expanduser('~'), '~')
                        f_list.append(os.path.join(n_path, name))

                # Need root and dirs to walk the directory; but they're not used
                # This is a throw-away branch to prevent a SyntasticCheck
                # warning
                if dirs == "" or root == "":
                    pass
        else:
            raise Exception('No trackable (.tex or .txt) files found.')

        # Correct the list by removing ignored files
        i_list = self.get_ignored()
        for file in i_list:
            if file in f_list:
                f_list.remove(file)
        return f_list

    def file_list(self):
        """Return a list of project file names"""
        f_list = []
        file_paths = self.filepath_list()
        for file in file_paths:
            path = os.path.expanduser(file)
            f_list.append(path)
        return f_list

    def n_tracked(self):
        """Return the number of files tracked in this project"""
        return len(self.filepath_list())

    def write_project(self):
        """Write project details to projects.dat"""
        with open(projects_path, "a") as proj:
            proj.write(self.p_name + ', ' + self.path + '\n')
        p_type = 'file' if self.is_file() else 'directory'
        msg = "The {} {} is being tracked as {}".format(p_type, self.path, self.p_name)
        return msg
