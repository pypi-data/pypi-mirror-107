#!/usr/bin/env python3
"""Functions to track writing progress."""
import os
import os.path
import re
from pathlib import Path
from src.trak.project import Project

projects_path = Path(__file__).parent / "../data/projects.dat"
sessions_path = Path(__file__).parent / "../data/sessions.dat"
ignore_path = Path(__file__).parent / "../data/ignore.dat"
tmp_path = Path(__file__).parent / "../data/tmp.dat"


class File(Project):
    """A writing document"""
    NAF_MSG = 'Not a file where one was expected'

    def name(self):
        """Return the base file name from path"""
        path = os.path.expanduser(self.path)
        return os.path.basename(path)

    def html_word_count(self):
        """Strip HTML tags and return the text word count"""
        counter = 0
        with open(os.path.expanduser(self.path), 'r') as txt:
            tagged_text = txt.readlines()
            for line in tagged_text:
                clean = re.compile('<.*?>')
                text = re.sub(clean, '', line)
                counter += len(text.split())
        return counter

    def word_count(self):
        """Return the file's word count"""
        if self.path.endswith('.html'):
            counter = self.html_word_count()
        else:
            with open(os.path.expanduser(self.path), 'r') as file:
                counter = len(file.read().split())
        return counter
