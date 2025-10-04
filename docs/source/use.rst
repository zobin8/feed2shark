Use feed2shark
==============
After the configuration of feed2shark, just launch the following command::

    $ feed2shark -c /path/to/feed2shark.ini

Run feed2shark on a regular basis
---------------------------------
feed2shark should be launched on a regular basis in order to efficiently send your new RSS entries to Sharkey. It is quite easy to achieve by adding a line to your user crontab, as described below::

    @hourly feed2shark -c /path/to/feed2shark.ini

will execute feed2shark every hour. Or without the syntactic sugar in the global crontab file /etc/crontab::

    0 * * * * janedoe feed2shark -c /path/to/feed2shark.ini

Test option
-----------
In order to know what's going to be sent to Sharkey without actually doing it, use the **--dry-run** option::

    $ feed2shark --dry-run -c /path/to/feed2shark.ini

Debug option
------------
In order to increase the verbosity of what's feed2shark is doing, use the **--debug** option followed by the level of verbosity see [the the available different levels](https://docs.python.org/3/library/logging.html)::

    $ feed2shark --debug -c /path/to/feed2shark.ini

Populate the cache file without posting toots
---------------------------------------------
Starting from 0.8, feed2shark offers the **--populate-cache** command line option to populate the cache file without posting to Sharkey::

    $ feed2shark --populate-cache -c feed2shark.ini
    populating RSS entry hhttps://xkcd.com/rss/65krkk
    populating RSS entry hhttps://xkcd.com/rss/co2es0
    populating RSS entry hhttps://xkcd.com/rss/la2ihl
    populating RSS entry hhttps://xkcd.com/rss/stfwtx
    populating RSS entry hhttps://xkcd.com/rss/qq1wte
    populating RSS entry hhttps://xkcd.com/rss/y8mzrp
    populating RSS entry hhttps://xkcd.com/rss/ozjqv0
    populating RSS entry hhttps://xkcd.com/rss/6ev8jz
    populating RSS entry hhttps://xkcd.com/rss/gezvnv
    populating RSS entry hhttps://xkcd.com/rss/lqswmz

How to display available sections of the rss feed
-------------------------------------------------
Starting from 0.8, feed2shark offers the **--rss-sections** command line option to display the available section of the rss feed and exits::

    $ feed2shark --rss-sections -c feed2shark.ini
    The following sections are available in this RSS feed: ['title', 'comments', 'authors', 'link', 'author', 'summary', 'links', 'tags', id', 'author_detail', 'published'].

Using syslog
------------
feed2shark is able to send its log to syslog. You can use it with the following command::

    $ feed2shark --syslog=WARN -c /path/to/feed2shark.ini

Limit number of rss entries published at each execution
-------------------------------------------------------
If you want to limit the number of rss entries published at each execution, you can use the --limit CLI option.

    $ feed2shark --limit 5 -c /path/to/feed2shark.ini

The number of posts to Sharkey will be at 5 posts top with this CLI option.
