# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright 2025 zobin8
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

'''Build the message'''

# standard libraires imports
import logging

# external liraries imports
from bs4 import BeautifulSoup
from bs4 import element
import feedparser
import requests
import mimetypes

# app libraries imports
from feed2shark.addtags import AddTags
from feed2shark.removeduplicates import RemoveDuplicates
from feed2shark.tootpost import TootPost

def strip_mfm(text):
    '''strip markup characters'''
    return ''.join([ch for ch in text if ch not in '[]() '])

def build_message_item(item, images):
    '''parse an item from an entry with unknown type recursively'''
    if type(item) == list:
        return ''.join([build_message_item(elem, images) for elem in item])
    elif type(item) == feedparser.util.FeedParserDict:
        return build_message_item(BeautifulSoup(item['value'], 'html.parser').contents, images)
    elif type(item) == element.Tag:
        if item.name == 'a' and 'href' in item.attrs:
            contents = strip_mfm(build_message_item(item.contents, images))
            if len(contents) == 0:
                return ''
            return f'[{contents}]({item.attrs["href"]})'
        elif item.name == 'p':
            return build_message_item(item.contents, images) + '\n\n'
        elif item.name == 'img' and 'src' in item.attrs:
            images.append(item.attrs)
            return ''
        elif item.name == 'br':
            return '\n\n'
        return build_message_item(item.contents, images)
    elif type(item) == element.NavigableString:
        return str(item)
    elif type(item) == str:
        return item

    return ''

def download_image(attrs):
    '''upload an image to Sharkey'''
    try:
        response = requests.get(attrs['src'])
        if response.status_code != 200:
            return None, None, None
        file_ext = ''
        if 'content-type' in response.headers:
            file_ext = mimetypes.guess_extension(response.headers['content-type']) or ''
        if 'alt' in attrs:
            return f'attached{file_ext}', response.content, attrs['alt']
        return f'attached{file_ext}', response.content, None
    except:
        return None, None, None

def build_message(entrytosend, tweetformat, rss, tootmaxlen, notagsintoot):
    '''populate the rss dict with the new entry'''
    images = []
    items = {k: build_message_item(v, images) for k, v in entrytosend.items()}
    tweetwithnotag = tweetformat.format(**items)

    # Download images
    image_data = []
    for attrs in images:
        logging.info('Downloading image', attrs)
        name, img, alt = download_image(attrs)
        if name:
            image_data.append((name, img, alt))

    # replace line breaks
    tootwithlinebreaks = tweetwithnotag.replace('\\n', '\n')
    # remove duplicates from the final tweet
    dedup = RemoveDuplicates(tootwithlinebreaks)
    # only add tags if user wants to
    if not notagsintoot:
        # only append hashtags if they exist
        # remove last tags if tweet too long
        if 'hashtags' in rss:
            addtag = AddTags(dedup.finaltweet, rss['hashtags'])
            finaltweet = addtag.finaltweet
        else:
            finaltweet = dedup.finaltweet
    else:
        finaltweet = dedup.finaltweet
    # strip html tags
    finaltweet = BeautifulSoup(finaltweet, 'html.parser').get_text()
    # truncate toot to user-defined value whatever the content is
    if len(finaltweet) > tootmaxlen:
        finaltweet = finaltweet[0:tootmaxlen-1]
        return ''.join([finaltweet[0:-3], '...'])
    else:
        return finaltweet, image_data

def send_message_dry_run(config, entrytosend, finaltweet, image_data):
    '''simulate sending message using dry run mode'''
    if entrytosend:
        logging.warning('Would toot with visibility "{visibility}" and local_only "{local_only}": {toot} with {images}'.format(
            toot=finaltweet,
            images=len(image_data),
            visibility=config.get(
                'sharkey', 'toot_visibility',
                fallback='public'),
            local_only=config.get('sharkey', 'local_only', fallback='false') != 'false'))
    else:
        logging.debug('This rss entry did not meet pattern criteria. Should have not been sent')

def send_message(config, clioptions, options, entrytosend, finaltweet, cache, rss, image_data):
    '''send message'''
    storeit = True
    if entrytosend and not clioptions.populate:
        logging.debug('Tooting with visibility "{visibility}": {toot}'.format(
            toot=finaltweet,
            visibility=config.get(
                'sharkey', 'toot_visibility',
                fallback='public')))
        twp = TootPost(config, options, finaltweet, image_data)
        storeit = twp.storeit()
    else:
        logging.debug('populating RSS entry {}'.format(rss['id']))
    # in both cas we store the id of the sent tweet
    if storeit:
        cache.append(rss['id'])
