### Feed2toot

Feed2toot automatically parses rss feeds, identifies new posts and posts them on the [Mastodon](https://mastodon.social) social network.
For the full documentation, [read it online](https://feed2toot.readthedocs.io/en/latest/).

If you like Feed2toot, you can donate cryptocurrencies to support the development:

- BTC: 1AW12Zw93rx4NzWn5evcG7RNNEM2RSLmAC
- XMR: 82VFaMG55AnW1MDgsmKgwUShT2MaiSi7AUY9DQANf7BWK3HdQBKwz58EcxshAWZGkV2A3KPGN6vqRjjvQWsr4jf6Dhc2kEC

### Quick Install

* Install Feed2toot from PyPI

        # pip3 install feed2toot

* Install Feed2toot from sources
  *(see the installation guide for full details)
  [Installation Guide](http://feed2toot.readthedocs.io/en/latest/install.html)*


        # tar zxvf feed2toot-0.17.tar.gz
        # cd feed2toot
        # python3 setup.py install
        # # or
        # python3 setup.py install --install-scripts=/usr/bin

### Create the authorization for the Feed2toot app

* Just launch the following command::

        $ register_feed2toot_app

### Use Feed2toot

* Create or modify feed2toot.ini file in order to configure feed2toot:

        [mastodon]
        instance_url=https://mastodon.social
        user_credentials=feed2toot_usercred.txt
        client_credentials=feed2toot_clientcred.txt
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

* Launch Feed2toot

        $ feed2toot -c /path/to/feed2toot.ini

### Authors

* Carl Chenet <carl.chenet@ohmytux.com>
* Antoine Beaupré <anarcat@debian.org>
* First developed by Todd Eddy

### License

This software comes under the terms of the GPLv3+. Previously under MIT license. See the LICENSE file for the complete text of the license.
