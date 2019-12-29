Use Feed2toot
==============
After the configuration of Feed2toot, just launch the following command::

    $ feed2toot -c /path/to/feed2toot.ini

Run Feed2toot on a regular basis
=================================
Feed2toot should be launche on a regular basis in order to efficiently send your new RSS entries to Mastodon. It is quite easy to achieve with adding a line to your user crontab, as described below::

    @hourly feed2toot -c /path/to/feed2toot.ini

will execute feed2toot every hour. Or without the syntactic sugar in the global crontab file /etc/crontab::

    0 * * * * johndoe feed2toot -c /path/to/feed2toot.ini

Test option
===========
In order to know what's going to be sent to Mastodon without actually doing it, use the **--dry-run** option::

    $ feed2toot --dry-run -c /path/to/feed2toot.ini

Debug option
============
In order to increase the verbosity of what's Feed2toot is doing, use the **--debug** option followed by the level of verbosity see [the the available different levels](https://docs.python.org/3/library/logging.html)::

    $ feed2toot --debug -c /path/to/feed2toot.ini

Populate the cache file without posting tweets
==============================================
Starting from 0.8, Feed2toot offers the **--populate-cache** command line option to populate the cache file without posting to Mastodon::

    $ feed2toot --populate-cache -c feed2toot.ini
    populating RSS entry https://www.journalduhacker.net/s/65krkk
    populating RSS entry https://www.journalduhacker.net/s/co2es0
    populating RSS entry https://www.journalduhacker.net/s/la2ihl
    populating RSS entry https://www.journalduhacker.net/s/stfwtx
    populating RSS entry https://www.journalduhacker.net/s/qq1wte
    populating RSS entry https://www.journalduhacker.net/s/y8mzrp
    populating RSS entry https://www.journalduhacker.net/s/ozjqv0
    populating RSS entry https://www.journalduhacker.net/s/6ev8jz
    populating RSS entry https://www.journalduhacker.net/s/gezvnv
    populating RSS entry https://www.journalduhacker.net/s/lqswmz

How to display available sections of the rss feed
=================================================
Starting from 0.8, Feed2toot offers the **--rss-sections** command line option to display the available section of the rss feed and exits::

    $ feed2toot --rss-sections -c feed2toot.ini
    The following sections are available in this RSS feed: ['title', 'comments', 'authors', 'link', 'author', 'summary', 'links', 'tags', id', 'author_detail', 'published'].

Using syslog
============
Feed2toot is able to send its log to syslog. You can use it with the following command::

    $ feed2toot --syslog=WARN -c /path/to/feed2toot.ini

Limit number of rss entries published at each execution
=======================================================
If you want to limit the number of rss entries published at each execution, you can use the --limit CLI option.

    $ feed2toot --limit 5 -c /path/to/feed2toot.ini

The number of posts to Mastodon will be at 5 posts top with this CLI option.
