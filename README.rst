===========
 PhotoFUSE
===========

Thoughts on EXIF reader libraries
=================================

Dev Notes
=========

import pyexiv2
img = pyexiv2.ImageMetaData('~/tmp/20090426-193954-00.jpg')
img.read()
img['Exif.Image.Rating'].value
img['Iptc.Application2.Keywords'].values
