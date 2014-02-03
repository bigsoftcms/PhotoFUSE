#
import logging
import mimetypes
import os
from errno import *
from fuse import FuseOSError, LoggingMixIn, Operations
from PIL import Image, IptcImagePlugin
from threading import Lock

log = logging.getLogger('photofuse')

EXIF_IMAGE_RATING_RAW = 18246
IPTC_APPLICATION2_KEYWORDS_RAW = (2, 25)
RATING = 'Exif.Image.Rating'
TAGS = 'Iptc.Application2.Keywords'

def judge_visibility(path, rating=None, tags=None):
    mime = mimetypes.guess_type(path)[0]

    if mime == 'image/jpeg':
        meta = get_image_metadata(path)
        if rating and (rating > meta[RATING] or not meta[RATING]):
            return False
        if tags and tags.isdisjoint(meta[TAGS]):
            return False
    return True

def get_image_metadata(path):
    metadata = {'Exif.Image.Rating': None,
                'Iptc.Application2.Keywords': []}

    exif, iptc = None, None

    try:
        image = Image.open(path)
        exif = image._getexif()
        iptc = IptcImagePlugin.getiptcinfo(image)
        image = None
    except:
        log.error("Error loading metadata: %s" % path)

    if exif and exif.has_key(EXIF_IMAGE_RATING_RAW):
        metadata[RATING] = exif[EXIF_IMAGE_RATING_RAW]
    if iptc and iptc.has_key(IPTC_APPLICATION2_KEYWORDS_RAW):
        metadata[TAGS] = iptc[IPTC_APPLICATION2_KEYWORDS_RAW]
        if isinstance(metadata[TAGS], str):
            metadata[TAGS] = [metadata[TAGS]]
    metadata[TAGS] = set(metadata[TAGS])
    return metadata

class PhotoFilterOperations(LoggingMixIn, Operations):
    def __init__(self, root, rating=None, tags=None):
        self.rwlock = Lock()
        self.root = os.path.realpath(root)
        self.rating = rating
        self.tags = tags
        self.visibility_cache = {}

    def __call__(self, op, path, *args):
        return super(PhotoFilterOperations, self).__call__(op, self.root + path, *args)

    def is_visible(self, path):
        if not self.visibility_cache.has_key(path):
            visible = judge_visibility(path, self.rating, self.tags)
            self.visibility_cache[path] = visible
        return self.visibility_cache[path]

    def getattr(self, path, fh=None):
        if not self.is_visible(path):
            raise FuseOSError(ENOENT)
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 
                                                        'st_nlink', 'st_size', 'st_uid'))

    def open(self, path, flags):
        if not self.is_visible(path):
            raise FuseOSError(ENOENT)
        return os.open(path, flags)

    # def opendir(self, path):
    #     pass

    def read(self, path, size, offset, fh):
        if not self.is_visible(path):
            raise FuseOSError(ENOENT)
        with self.rwlock:
            os.lseek(fh, offset, 0)
            return os.read(fh, size)

    def readdir(self, path, fh):
        visible_files = ['.', '..']
        for f in os.listdir(path):
            if self.is_visible(os.sep.join([path, f])):
                visible_files.append(f)
        return visible_files

    # def readdlink(self, path):
    #     pass

    def release(self, path, fh):
        return os.close(fh)

    def statfs(self, path):
        if self.is_visible(path):
            stv = os.statvfs(path)
            return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                             'f_blocks', 'f_bsize', 
                                                             'f_favail', 'f_ffree', 
                                                             'f_files', 'f_flag',
                                                             'f_frsize', 'f_namemax'))
        return {}

    # def utimens(self, path, times=None):
    #     pass
