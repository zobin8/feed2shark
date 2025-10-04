### feed2shark

feed2shark automatically parses rss feeds, identifies new posts and posts them on the [Mastodon](https://mastodon.social) social network.
For the full documentation, [read it online](https://feed2shark.readthedocs.io/en/latest/).

If you like feed2shark, you can donate cryptocurrencies to support the development:

- BTC: 1AW12Zw93rx4NzWn5evcG7RNNEM2RSLmAC
- XMR: 82VFaMG55AnW1MDgsmKgwUShT2MaiSi7AUY9DQANf7BWK3HdQBKwz58EcxshAWZGkV2A3KPGN6vqRjjvQWsr4jf6Dhc2kEC

### Quick Install

* Install feed2shark from PyPI

        # pip3 install feed2shark

* Install feed2shark from sources
  *(see the installation guide for full details)
  [Installation Guide](http://feed2shark.readthedocs.io/en/latest/install.html)*


        # tar zxvf feed2shark-0.17.tar.gz
        # cd feed2shark
        # python3 setup.py install
        # # or
        # python3 setup.py install --install-scripts=/usr/bin

### Create the authorization for the feed2shark app

* Just launch the following command::

        $ register_feed2shark_app

### Use feed2shark

* Create or modify feed2shark.ini file in order to configure feed2shark:

        [mastodon]
        instance_url=https://mastodon.social
        user_credentials=feed2shark_usercred.txt
        client_credentials=feed2shark_clientcred.txt
        ; Default visibility is public, but you can override it:
        ; toot_visibility=unlisted
        ; Default local_only is false, but you can override it:
        ; local_only=true

        [cache]
        cachefile=cache.db

        [rss]
        uri=https://www.journalduhacker.net/rss
        toot={title} {link}

        [hashtaglist]
        several_words_hashtags_list=hashtags.txt

* Launch feed2shark

        $ feed2shark -c /path/to/feed2shark.ini

### Authors

* Carl Chenet <carl.chenet@ohmytux.com>
* Antoine Beaupré <anarcat@debian.org>
* First developed by Todd Eddy

### License

This software comes under the terms of the GPLv3+. Previously under MIT license. See the LICENSE file for the complete text of the license.
