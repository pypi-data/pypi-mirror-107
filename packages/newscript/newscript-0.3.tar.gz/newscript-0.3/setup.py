#setup.py
from setuptools import setup
import re

#change version number in ns file  add/edit version="DESIRED_VERSION NUMBER" at the top of file

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('newscript').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"


setup(
    name='newscript',
    scripts=['newscript'],
    version= version,
    description = 'shell script creator helper',
    long_description = long_descr,
    author = 'madhavth'
)
