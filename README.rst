===========
 PhotoFUSE
===========

`PhotoFUSE <https://github.com/timfreund/PhotoFUSE>`_ uses
`FUSE <http://fuse.sourceforge.net/>`_ and
`fusepy <https://github.com/terencehonles/fusepy>`_ along
with `PIL <https://pypi.python.org/pypi/PIL>`_ to expose a
subset of my photo collection as a virtual directory,
filtered by rating and tags.

Use it::

    $ photofuse --help
    Usage: photofuse [options]

    Options:
      -h, --help            show this help message and exit
      -s SOURCE, --source-dir=SOURCE
                            Photo directory
      -r RATING, --rating=RATING
                            Exif.Image.Rating
      -d DESTINATION, --destination=DESTINATION

    photofuse -r 3 -s /usr/data/Photos -d dest/ a_tag another_tag
