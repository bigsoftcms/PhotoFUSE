===========
 PhotoFUSE
===========

Thoughts on EXIF reader libraries
=================================

Dev Notes
=========

import mimetypes
import pyexiv2
mtype = mimetypes.guess_type('~/tmp/20090426-193954-00.jpg')[0]
img = pyexiv2.ImageMetadata('~/tmp/20090426-193954-00.jpg')
img.read()
img['Exif.Image.Rating'].value
img['Iptc.Application2.Keywords'].values
