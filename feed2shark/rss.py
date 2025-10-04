# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2015-2021 Carl Chenet <carl.chenet@ohmytux.com>
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

'''Manage a lock file'''

# standard libraires imports
import datetime
import logging
import os
import os.path
import sys

def populate_rss(entry):
    '''populate the rss dict with the new entry'''
    if 'id' in entry:
        logging.debug('found feed entry {entryid}'.format(entryid=entry['id']))
        rss = {
            'id': entry['id'],
        }
    elif 'guid' in entry:
        logging.debug('found feed entry {entryid}'.format(entryid=entry['guid']))
        rss = {
            'id': entry['guid'],
        }
    else:
        logging.debug('found feed entry {entryid}'.format(entryid=entry['link']))
        rss = {
            'id': entry['link'],
        }
    return rss
