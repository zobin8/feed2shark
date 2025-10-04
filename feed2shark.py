#!/usr/bin/env python3
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

# Launch Feed2toot
'''Launch Feed2toot'''

import sys
from feed2toot.main import Main

class Feed2Toot(object):
    '''Feed2toot class'''

    def __init__(self):
        '''Constructor of the Feed2Toot class'''
        self.main()

    def main(self):
        '''main of the Feed2Toot class'''
        Main()

if __name__ == '__main__':
    Main()
    sys.exit(0)
