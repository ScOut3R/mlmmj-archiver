mlmmj-archiver
==============

mlmmj-archiver is a wrapper around hypermail to manage the HTML archive generation of mlmmj-based mailing lists. It uses a YAML configuration file to describe the lists and their options.

This script was inspired by Martin Leopold's update-archive.sh script. You can his version on his [webpage](http://www.leopold.dk/~martin/mlmmj-scripts.html).

You can get support or request new features at the following [site](https://admin.modernbiztonsag.org/redmine/projects/mlmmj-archiver).

Installation
------------
### Package ###
    easy_install mlmmj_archiver
    
### Source ###
Get it from [github](https://github.com/ScOut3R/mlmmj-archiver).


Configuration syntax
--------------------
    list-name:
     archive: /path/to/archive/dir
     list: /path/to/list/dir
     options:
      ordering: thread
      threadlevels: 100
      index: monthly
      output:
       - showreplies

All the options are optional. The supported output options are shown above, further options will be added soon.

Usage
-----
    mlmmj_archiver.py [-h] [-c CONFIG] [-x] [-p]

    optional arguments:
     -h, --help            show this help message and exit
     -c CONFIG, --config CONFIG
                           use alternate config file (default: /etc/mlmmj-archiver/config.yml)
     -x, --overwrite       overwrite archives
     -p, --progress        show progress

