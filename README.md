### feed2shark

feed2shark automatically parses rss feeds, identifies new posts and posts them on a Sharkey instance.

### Quick Install

* Install feed2shark from PyPI

        # pip3 install feed2shark

* Install feed2shark from sources

        # tar zxvf feed2shark-0.18.tar.gz
        # cd feed2shark
        # python3 -m venv .venv
        # source .venv/bin/activate
        # pip install .

### Create the API token for the feed2shark app:

* On your Sharkey account, navigate to the Settings menu
* Select the "Service Integration" section
* Click "Generate Access Token"
* Check the "Edit or delete your Drive files and folders" option
* Check the "Compose or delete notes" option
* Create the token and save it to a text file (e.g. feed2shark_usercred.txt)

### Use feed2shark

* Create or modify feed2shark.ini file in order to configure feed2shark:

        [mastodon]
        instance_url=https://blahaj.zone
        user_credentials=feed2shark_usercred.txt
        ; Default visibility is public, but you can override it:
        ; toot_visibility=unlisted
        ; Default local_only is false, but you can override it:
        ; local_only=true

        [cache]
        cachefile=cache.db

        [rss]
        uri=https://xkcd.com/rss
        toot={title} {link}

        [hashtaglist]
        several_words_hashtags_list=hashtags.txt

* Launch feed2shark

        $ feed2shark -c /path/to/feed2shark.ini

### Authors

* zobin8

Based on feed2toot by:
* Carl Chenet <carl.chenet@ohmytux.com>
* Antoine Beaupré <anarcat@debian.org>
* First developed by Todd Eddy

### License

This software comes under the terms of the GPLv3+. Previously under MIT license. See the LICENSE file for the complete text of the license.
