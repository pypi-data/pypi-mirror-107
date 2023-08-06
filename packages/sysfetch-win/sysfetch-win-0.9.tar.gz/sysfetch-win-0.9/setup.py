import re
import os
from os import path
from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


version = ''
with open('sysfetch_win/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


if not version:
    raise RuntimeError('not a valid version')




setup(
    name='sysfetch-win',
    author='NandyDark',
    url='https://github.com/nandydark/sysfetch-win',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=['sysfetch_win'],
    license='MIT Licence',
    description='Fetch Info About Your Windows System',
    keywords=['sysfetch', 'sysfetch-win', 'nandydark', 'neofetch', 'neofetch-win'],
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'sysfetch=sysfetch_win.main:main'
        ]
    }
)
