# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright 2025 ZoeOfShark
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

"""Checks an RSS feed and posts new entries to Mastodon."""

# 3rd party libraries imports
import requests
import logging

class TootPost:
    '''TootPost class'''

    def __init__(self, config, options, toot):
        '''Constructore of the TootPost class'''
        self.config = config
        self.options = options
        self.store = True
        self.toot = toot
        self.main()

    def main(self):
        '''Main of the TweetPost class'''
        
        instance = self.config.get('mastodon', 'instance_url')
        usercredfile = self.config.get('mastodon', 'user_credentials')
        toot_visibility = self.config.get('mastodon', 'toot_visibility', fallback='public')
        local_only = self.config.get('mastodon', 'local_only', fallback='false') != 'false'

        # ZTODO: Cache file contents
        with open(usercredfile, 'r', encoding='utf-8') as f:
            token = f.read().strip()
            headers = dict(Authorization='Bearer ' + token)

        media_ids = []
        if 'custom' in self.options['media']:
            # ZTODO: Upload media
            response = requests.post(f'{instance}/api/drive/files/create', headers=headers, files=dict())
            media_ids.append(response['createdNote']['id'])
        else:
            # ZTODO: Use module for sharkey API
            response = requests.post(f'{instance}/api/notes/create', headers=headers, json=dict(
                text=self.toot,
                localOnly=local_only,
                visibility=toot_visibility,
            ))
            if response.status_code != 200:
                logging.error(response.status_code, response.json())

    def storeit(self):
        '''Indicate if the tweet should be stored or not'''
        return self.store
