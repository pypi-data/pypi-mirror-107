#setup.py
from setuptools import setup

f= open("version", "r")
version=f.read()

setup(
    name='shellpackager',
    scripts=['shellpackager'],
    version= '0.8',
    description = 'simple project, simple life',
    long_description = 'cli tool to create pypi project from shell scripts',
      install_requires=[
          'twine',
          'setuptools'
      ],
    author = 'madhavth'
)
