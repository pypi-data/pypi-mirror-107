import codecs
import os
import re
from setuptools import find_packages, setup

def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
)

install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

setup(
    name='myKGlib',
    packages=['myKGlib', 'myKGlib.charts', 'myKGlib.utils'],
    version='0.0.0.8',
    description='VizKG',
    author='Hana',
    install_requires=install_reqs,
    license='MIT',
)