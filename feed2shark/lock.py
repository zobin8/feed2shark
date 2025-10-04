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

class LockFile:
    '''LockFile object'''
    def __init__(self, lockfile, locktimeout):
        '''check the lockfile and the locktimeout'''
        self.lockfile = lockfile
        ltimeout = datetime.timedelta(seconds=locktimeout)
        self.lfdateformat = '%Y-%m-%d_%H-%M-%S'
        # if a lock file exists
        if os.path.exists(self.lockfile):
            if os.path.isfile(self.lockfile):
                with open(self.lockfile, 'r') as lf:
                    lfcontent = lf.read().rstrip()
                # lfcontent should be a datetime
                logging.debug('Check if lock file is older than timeout ({timeout} secs)'.format(timeout=locktimeout))
                locktime = datetime.datetime.strptime(lfcontent, self.lfdateformat)
                if locktime < (datetime.datetime.now() - ltimeout):
                    # remove the lock file
                    logging.debug('Found an expired lock file')
                    self.release()
                    self.create_lock()
                else:
                    # quit because another feed2toot process is running
                    logging.debug('Found a valid lock file. Exiting immediately.')
                    sys.exit(0)
        else:
            # no lock file. Creating one
            self.create_lock()

    def create_lock(self):
        '''Create a lock file'''
        with open(self.lockfile, 'w') as lf:
            currentdatestring = datetime.datetime.now().strftime(self.lfdateformat)
            lf.write(currentdatestring)
            logging.debug('lockfile {lockfile} created.'.format(lockfile=self.lockfile))

    def release(self):
        '''Release the lockfile'''
        os.remove(self.lockfile)
        logging.debug('Removed lock file.')
