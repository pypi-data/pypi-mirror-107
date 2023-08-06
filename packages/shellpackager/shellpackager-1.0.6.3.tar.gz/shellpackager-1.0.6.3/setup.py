#setup.py
from setuptools import setup
import re

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('shellpackager').read(),
    re.M
)


if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"

print("version is " + version)

setup(
    name='shellpackager',
    scripts=['shellpackager'],
    version= version,
    description = 'simple project, simple life',
    long_description = 'cli tool to create pypi project from shell scripts',
      install_requires=[
          'twine',
          'setuptools',
          'wheel'
      ],
    author = 'madhavth'
)
