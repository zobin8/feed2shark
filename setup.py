# Copyright 2015-2021 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#!/usr/bin/env python3

# Setup for feed2shark
'''Setup for feed2shark'''

from setuptools import setup, find_packages

CLASSIFIERS = [
    'Intended Audience :: End Users/Desktop',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
]

setup(
    name='feed2shark',
    version='0.18',
    license='GNU GPL v3',
    description='Parse rss feeds and send new posts to Sharkey',
    long_description='Parse rss feeds and send new posts to the Sharkey API',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    scripts=['scripts/feed2shark'],
    install_requires=['beautifulsoup4', 'feedparser', 'requests'],
    extras_require={
        'influxdb':  ["influxdb"]
    }
)
