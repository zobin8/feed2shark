Configure feed2shark
===================

Create the API token for Sharkey
-------------------------------
As a prerequisite to use feed2shark, you need to authorize a Sharkey app for your account.

* On your Sharkey account, navigate to the Settings menu
* Select the "Service Integration" section
* Click "Generate Access Token"
* Check the "Edit or delete your Drive files and folders" option
* Check the "Compose or delete notes" option
* Create the token and save it to a text file (e.g. feed2shark_usercred.txt)

Create feed2shark configuration
------------------------------
In order to configure feed2shark, you need to create a feed2shark.ini file (or any name you prefer, finishing with the extension .ini) with the following parameters::

    [sharkey]
    instance_url=https://blahaj.zone
    ; Here you need the two files created by register_feed2shark_app
    user_credentials=/etc/feed2shark/credentials/feed2shark_usercred.txt
    ; Default visibility is public, but you can override it:
    ; toot_visibility=unlisted
    ; Default local_only is false, but you can override it:
    ; local_only=true

    [cache]
    cachefile=/var/lib/feed2shark/feed2shark.db
    cache_limit=10000

    [lock]
    lock_file=/var/lock/feed2shark.lock
    lock_timeout=3600

    [rss]
    uri=https://xkcd.com/rss
    uri_list=/etc/feed2shark//rsslist.txt
    toot={title} {link}
    ; toot_max_len=125000
    title_pattern=Open Source
    title_pattern_case_sensitive=true
    no_uri_pattern_no_global_pattern=true
    ; ignore_ssl=false

    [hashtaglist]
    several_words_hashtags_list=/etc/feed2shark/hashtags.txt
    ; no_tags_in_toot=false

    [feedparser]
    accept_bozo_exceptions=true

    [media]
    custom=/var/lib/feed2shark/media/logo.png

For the [sharkey] section:

- instance_url: the url of your Sharkey instance
- user_credentials: a file with the API token, generated earlier
- toot_visibility: any of the valid options for the *visibility* field
  `here`__.
  Default is *public*, but *unlisted* prevents flooding
  the instance's public timeline (which is more polite).
- local_only: should be "true" or "false". If true, will prevent federating your toots

__ https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md#posting-a-new-status

For the [cache] section:

- cachefile: the path to the cache file storing ids of already tooted links. Absolute path is mandatory. This file should always use the .db extension.
- cache_limit: length of the cache queue. defaults to 100.

For the [lock] section (starting from version 0.11):

- lock_file: lock to stop any other feed2shark instance to run at the same time. Default is ~/.config/feed2shark.lock
- lock_timeout: automatically remove the lock if the datetime in the lock file is greater than n seconds. Default is 3600 seconds.

For the [rss] section:

- uri: the url of the rss feed to parse
- uri_list: a path to a file with several adresses of rss feeds, one by line. Absolute path is mandatory.
- toot: format of the toot you want to post. It should use existing entries of the RSS fields like {title} or {link}. Launch it with this field empty to display all available entries. If you want to shorten the size of a field, you can use the syntax {summary:.100} to cut the field "summary" of the rss feed after the first 100 characters (starting from version 0.10). To add new lines you can use \\n (starting from version 0.14)
- toot_max_len: the max length of a toot can be defined here. If the toot size is longer, the toot is truncated and "..." added at the end. Defaults is 500 characters.
- {one field of the rss feed}_pattern: takes a string representing a pattern to match for a specified field of each rss entry of the rss feed, like title_pattern or summary_pattern.
- {one field of the rss feed}_pattern_case_sensitive: either the pattern matching for the specified field should be case sensitive or not. Default to true if not specified.
- no_uri_pattern_no_global_pattern: don't apply global pattern (see above) when no pattern-by-uri is defined in the uri_list. Allows to get all entries of a rss in the uri_list because no pattern is defined so we match them all. Defaults to false, meaning the global patterns will be tried on every rss in the uri_list NOT HAVING specific patterns and so ONLY entries from the specific uri in the uri_list matching the global patterns will be considered.
- addtags: add the tags from the rss feed at the end of the toot. Defaults to true.
- ignore_ssl: when the uri or uri_list contains an https url with an invalid certificate (e.g an expired one), feed2shark will be unable to get rss content. This option allows to bypass the ssl security to catch the rss content. Defaults to false.

For the [hashtaglist] section:

- several_words_hashtags_list: a path to the file containing hashtags in two or more words. Absolute path is mandatory. By default feed2shark adds a # before every words of a hashtag. See documentation below for an example of this file.
- no_tags_in_toot: stop hash tags to be added at the toot. Defaults to false.

for the [feedparser] section:

- accept_bozo_exceptions: If set to true, feed2shark will accept malformed feeds, which are rejected by default.

For the [media] section:

- custom: the path to a media (should be supported by Sharkey) to be posted with every Sharkey post.

Example of the list of hash tags
================================
The list of hash tags is a simple text file with one hash tag composed by several words on a single line::

    free software community
    open-source

Instead of having #free #software #community or #open-source in the resulting toot, you will have #freesoftwarecommunity and #opensource. You only have to identify the hash tags you frequently use in your RSS feeds and put them in this file to have well formatted hash tags in your toots.

List of rss feeds
=================
Simple list of rss feeds
------------------------
With the parameter **uri_list**, you can define a list of uri to use. feed2shark is able to match specific patterns for each of the rss feeds from this list. Consider the following rss section of the configuration file::

    [rss]
    uri_list=/home/jane/feed2shark/rsslist.txt
    toot={title} {link}

Now let's have a look at the =/home/jane/feed2shark/rsslist.txt file::

    https://xkcd.com/rss
    https://www.erininthemorning.com/feed

Each line of this file is a url to a rss feed. Pretty simple.

Display the name of the feed in the toots
-----------------------------------------

If you want to display the name of the feed in the resulting toot, you can do so by giving it a name with the following syntax::

    XKCD <https://xkcd.com/rss>

Then in the `toot` configuration, you can use the `{feedname}` syntax, which will be replaced by the actual name of the feed.

Match specific patterns of rss feeds in the uri_list files
----------------------------------------------------------
You can use specific pattern matching for uri in the uri_list file to filter some of the rss entries of a rss feed. Lets modify the previous file::

    https://xkcd.com/rss|title|hacker,psql
    https://www.erininthemorning.com/feed|title|gitlab

Each line of this file starts with an uri, followed by a pipe (|), followed by the name of the available section to parse (see below), again followed by a pipe (|), followed by patterns, each pattern being separated from the other one by a semi-colon (,).

In the example file above wee get every rss entries from the feed available at https://xkcd.com/rss where a substring in the title section of this entry matches either "hacker" or "psql". Specific patterns are not case sensitive. For the second line, we match every rss entries from the feed available at https://carlchenet.com/feed where a substring in the title section of this entry matches "gitlab".

Consider every entries of a rss feed from a uri in the uri_list file
--------------------------------------------------------------------
It is possible to get all entries from a rss feed available in the uri_list file. You need an option to deactivate the global pattern matching for uri in the uri_list NOT having specific patterns::

    [rss]
    ...
    no_uri_pattern_no_global_pattern=true

In you rsslist.txt, just don't give anything else than the needed feed url to get all the entries::

    https://xkcd.com/rss|title|hacker,psql
    https://www.erininthemorning.com/feed|title|gitlab
    https://blog.linuxjobs.fr/feed.php?rss

The last line of the file above only has the url of a rss feed. All entries from this feed will be tooted.
