from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="trak",
    version="0.1.2",
    author="Greg Pyle",
    author_email="chaoborid@gmail.com",
    description="A simple writing-progress tracking tool for plain text files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=['LICENSE'],
    download_url="https://github.com/Gambusia/trak",
    packages=["src", "src.trak"],
    package_data={'src': ['data/*.dat']},
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Office/Business',
          'Topic :: Text Editors :: Text Processing',
          'Topic :: Text Processing :: General',
          'Topic :: Utilities',
          'Typing :: Typed',
          ],
    entry_points={
        "console_scripts": [
            "trak = src.__main__:main"
        ]
    },
)
