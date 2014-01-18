#
import mimetypes
from errno import *
from fuse import Operations
from PIL import Image, IptcImagePlugin

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
    image = Image.open(path)
    exif = image._getexif()
    iptc = IptcImagePlugin.getiptcinfo(image):

    if exif.has_key(EXIF_IMAGE_RATING_RAW):
        metadata[RATING] = exif[EXIF_IMAGE_RATING_RAW]
    if iptc and iptc.has_key(IPTC_APPLICATION2_KEYWORDS_RAW):
        metadata[TAGS] = iptc[IPTC_APPLICATION2_KEYWORDS_RAW]
        if isinstance(metadata[TAGS], str):
            metadata[TAGS] = [metadata[TAGS]]
    metadata[TAGS] = set(metadata[TAGS])
    return metadata

class PhotoFilterOperations(Operations):
    def __init__(self, root, rating=None, tags=None):
        self.root = root
        self.rating = rating
        self.tags = tags

    def __call__(self, op, path, *args):
        return super(PhotoFilterOperations, self).__call__(op, self.root + path, *args)

    def getattr(self, path, fh=None):
        pass

    def open(self, path, flags):
        pass

    def opendir(self, path):
        pass

    def read(self, path, size, offset, fh):
        pass

    def readdir(self, path, fh):
        pass

    def readdlink(self, path):
        pass

    def statfs(self, path):
        pass

    def utimens(self, path, times=None):
        pass
