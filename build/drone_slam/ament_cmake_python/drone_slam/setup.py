from setuptools import find_packages
from setuptools import setup

setup(
  name='drone_slam',
  version='0.1.0',
  packages=find_packages(
      include=('drone_slam', 'drone_slam.*')),
)
