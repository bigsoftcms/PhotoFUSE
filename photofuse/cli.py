import mimetypes
import os
import sys

from fuse import FUSE
from optparse import OptionParser, Option
from photofuse import PhotoFilterOperations, judge_visibility, get_image_metadata, RATING, TAGS

def validate_destination(options, args):
    if not options.destination:
        print "A destination is required"
        return False
    return True

def validate_rating(options, args):
    if options.rating:
        options.rating = int(options.rating)
    return True

def validate_source(options, args):
    if not options.source:
        print "A source is required"
        return False
    return True

def validate_tags(options, args):
    if args:
        options.tags = set(args)
    else:
        options.tags = None
    return True

def parse_options(options=[], validators=[], usage=None):
    validators.insert(0, validate_source)
    validators.insert(0, validate_rating)
    validators.insert(0, validate_tags)

    parser = OptionParser()
    parser.add_option('-s', '--source-dir', dest='source', help='Photo directory')
    parser.add_option('-r', '--rating', dest='rating', help='Exif.Image.Rating')

    for option in options:
        parser.add_option(option)

    if usage:
        parser.usage = usage

    (options, args) = parser.parse_args()
    for validator in validators:
        if not validator(options, args):
            parser.print_help()
            sys.exit(-1)
        
    return options, args

def ls(argv=sys.argv):
    (opts, args) = parse_options()
    print "Search %s" % opts.source
    if opts.rating:
        print "\twith rating >= %s" % opts.rating

    if args:
        print "\twith the tag(s): %s" % " ".join(args)

    for dirpath, dirnames, filenames in os.walk(opts.source):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            if mimetypes.guess_type(full_path)[0] == 'image/jpeg':
                if judge_visibility(full_path, opts.rating, opts.tags):
                    meta = get_image_metadata(full_path)
                    print "%s Rating(%s) Tags(%s)" % (full_path, meta[RATING], ", ".join(meta[TAGS]))

def photofuse(argv=sys.argv):
    opts, args = parse_options([Option('-d', '--destination', dest='destination')], 
                               validators=[validate_destination])
    FUSE(PhotoFilterOperations(opts.source, opts.rating, opts.tags),
         opts.destination, foreground=True)


