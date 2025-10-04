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
import codecs

def extract_hashtags_from_list(options):
    '''extract hashtags from the the list''' 
    if 'hashtaglist' in options and options['hashtaglist']:
        severalwordshashtags = codecs.open(options['hashtaglist'],
                                           encoding='utf-8').readlines()
        severalwordshashtags = [i.rstrip('\n') for i in severalwordshashtags]
    else:
        severalwordshashtags = []
    return severalwordshashtags

def build_hashtags(entry, rss, options, severalwordshashtags):
    '''build hashtags'''
    severalwordsinhashtag = False
    # has the the rss feed hashtag
    if 'tags' in entry and options['addtags']:
        hastags = True
    else:
        hastags = False
    if hastags:
        rss['hashtags'] = []
        for i, _ in enumerate(entry['tags']):
            if 'hashtaglist' in options:
                prehashtags = entry['tags'][i]['term']
                tmphashtags = entry['tags'][i]['term']
                for element in severalwordshashtags:
                    if element in prehashtags:
                        severalwordsinhashtag = True
                        tmphashtags = prehashtags.replace(element,
                                                          ''.join(element.split()))
            # replace characters stopping a word from being a hashtag
            if severalwordsinhashtag:
                # remove ' from hashtag
                tmphashtags = tmphashtags.replace("'", "")
                # remove - from hashtag
                tmphashtags = tmphashtags.replace("-", "")
                # remove . from hashtag
                tmphashtags = tmphashtags.replace(".", "")
                # remove space from hashtag
                finalhashtags = tmphashtags.replace(" ", "")
                rss['hashtags'].append('#{}'.format(finalhashtags))
            else:
                nospace = ''.join(entry['tags'][i]['term'])
                # remove space from hashtag
                nospace = nospace.replace(" ", "")
                rss['hashtags'].append('#{}'.format(nospace))
    return rss
