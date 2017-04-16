#!/usr/bin/env python3
# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2015-2017 Carl Chenet <carl.chenet@ohmytux.com>
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

# standard libraires imports
import codecs
import importlib
import logging
import logging.handlers
import os
import sys

# 3rd party libraries imports
import feedparser

# app libraries imports
from feed2toot.addtags import AddTags
from feed2toot.cliparse import CliParse
from feed2toot.confparse import ConfParse
from feed2toot.filterentry import FilterEntry
from feed2toot.removeduplicates import RemoveDuplicates
from feed2toot.tootpost import TootPost
from feed2toot.feedcache import FeedCache

class Main(object):
    '''Main class of Feed2toot'''

    def __init__(self):
        self.main()

    def setup_logging(self, options):
        if options.syslog:
            sl = logging.handlers.SysLogHandler(address='/dev/log')
            sl.setFormatter(logging.Formatter('feed2toot[%(process)d]: %(message)s'))
            # convert syslog argument to a numeric value
            loglevel = getattr(logging, options.syslog.upper(), None)
            if not isinstance(loglevel, int):
                raise ValueError('Invalid log level: %s' % loglevel)
            sl.setLevel(loglevel)
            logging.getLogger('').addHandler(sl)
            logging.debug('configured syslog level %s' % loglevel)
        logging.getLogger('').setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(options.log_level.upper())
        logging.getLogger('').addHandler(sh)
        logging.debug('configured stdout level %s' % sh.level)

    def main(self):
        """The main function."""
        clip = CliParse()
        clioptions = clip.options
        self.setup_logging(clioptions)
        # iterating over the different configuration files
        cfgp = ConfParse(clioptions)
        confs = cfgp.confvalues
        for conf in confs:
            options = conf[0]
            config = conf[1]
            tweetformat = conf[2]
            feeds = conf[3]
            plugins = conf[4]
            # create link to the persistent list
            cache = FeedCache(options)
            if options['hashtaglist']:
                severalwordshashtags = codecs.open(options['hashtaglist'],
                                                   encoding='utf-8').readlines()
                severalwordshashtags = [i.rstrip('\n') for i in severalwordshashtags]
            # reverse feed entries because most recent one should be sent as the last one in Mastodon
            for feed in feeds:
                # store the patterns by rss
                if 'patterns' in feed:
                    patterns = feed['patterns']
                entries = feed['feed']['entries'][0:clioptions.limit]
                entries.reverse()
                # --rss-sections option: print rss sections and exit
                if clioptions.rsssections:
                    if entries:
                        print('The following sections are available in this RSS feed: {}'.format([j for j in entries[0]]))
                        sys.exit(0)
                    else:
                        sys.exit('Could not parse the section of the rss feed')
                totweet = []
                # cache the ids of last rss feeds
                if not clioptions.all:
                    for i in entries:
                        if 'id' in i and i['id'] not in cache.getdeque():
                            totweet.append(i)
                else:
                    totweet = entries

                for entry in totweet:
                    if 'id' not in entry:
                        # malformed feed entry, skip
                        continue
                    #logging.debug('found feed entry %s, %s', entry['id'], entry['title'])


                    rss = {
                        'id': entry['id'],
                    }

                    severalwordsinhashtag = False
                    # lets see if the rss feed has hashtag
                    if 'tags' in entry:
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

                    elements=[]
                    for i in tweetformat.split(' '):
                        tmpelement = ''
                        # if i is not an empty string
                        if i:
                            if i.startswith('{') and i.endswith('}'):
                                tmpelement = i.strip('{}')
                                elements.append(tmpelement)
                    # match elements of the tweet format string with available element in the RSS feed
                    fe = FilterEntry(elements, entry, options, feed['patterns'], feed['rssobject'])
                    entrytosend = fe.finalentry
                    if entrytosend:
                        tweetwithnotag = tweetformat.format(**entrytosend)
                        # remove duplicates from the final tweet
                        dedup = RemoveDuplicates(tweetwithnotag)
                        # only append hashtags if they exist
                        # remove last tags if tweet too long
                        if 'hashtags' in rss:
                            addtag = AddTags(dedup.finaltweet, rss['hashtags'])
                            finaltweet = addtag.finaltweet
                        else:
                            finaltweet = dedup.finaltweet
                        
                    if clioptions.dryrun:
                        if entrytosend:
                            logging.warning('Tweet should have been sent: {tweet}'.format(tweet=finaltweet))
                        else:
                            logging.debug('This rss entry did not meet pattern criteria. Should have not been sent')
                    else:
                        storeit = True
                        if entrytosend and not clioptions.populate:
                            logging.debug('sending the following tweet:{tweet}'.format(tweet=finaltweet))
                            twp = TootPost(config, finaltweet)
                            storeit = twp.storeit()
                        else:
                            logging.debug('populating RSS entry {}'.format(rss['id']))
                        # in both cas we store the id of the sent tweet
                        if storeit:
                            cache.append(rss['id'])
                        # plugins
                        if plugins and entrytosend:
                            for plugin in plugins:
                                capitalizedplugin = plugin.title()
                                pluginclassname = '{plugin}Plugin'.format(plugin=capitalizedplugin)
                                pluginmodulename = 'feed2toot.plugins.{pluginmodule}'.format(pluginmodule=pluginclassname.lower())
                                try:
                                    pluginmodule = importlib.import_module(pluginmodulename)
                                    pluginclass = getattr(pluginmodule, pluginclassname) 
                                    pluginclass(plugins[plugin], finaltweet)
                                except ImportError as err:
                                    print(err)
            # do not forget to close cache (shelf object)
            cache.close()
