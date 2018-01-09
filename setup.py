import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "wrapc",
    version = "0.0.1",
    author = "Dick Marinus",
    author_email = "dick@mrns.nl",
    description = ("Wrapper script for starting a command line tool with bash completion"),
    license = "GPL-3",
    keywords = "cli bash-completion",
    url = "https://github.com/meeuw/wrapc",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL-3 License",
    ],
    packages=['.'],
    entry_points={'console_scripts': ['wrapc = wrapc']},
    install_requires=[
        'argparse',
        'argcomplete',
    ]
)
