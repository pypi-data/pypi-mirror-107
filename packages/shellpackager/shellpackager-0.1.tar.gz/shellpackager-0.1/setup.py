#setup.py
from setuptools import setup

setup(
    name='shellpackager',
    scripts=['shellpackager'],
    version= '0.1',
    description = 'simple project, simple life',
    long_description = 'cli tool to create pypi project from shell scripts',
      install_requires=[
          'twine'
      ],
    author = 'madhavth'
)
