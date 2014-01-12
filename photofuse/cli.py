import mimetypes
import os
import pyexiv2
import sys

from optparse import OptionParser, Option

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
                visible = True
                rating = None
                tags = []

                img = pyexiv2.ImageMetadata(full_path)
                img.read()

                if img.keys().count('Exif.Image.Rating'):
                    rating = img['Exif.Image.Rating'].value
                if img.keys().count('Iptc.Application2.Keywords'):
                    tags = img['Iptc.Application2.Keywords'].values
                
                if opts.rating and (opts.rating > rating or not rating):
                    visible = False

                if opts.tags and opts.tags.isdisjoint(set(tags)):
                    visible = False
                    
                if visible:
                    print "%s Rating(%s) Tags(%s)" % (full_path, rating, ", ".join(tags))

def photofuse(argv=sys.argv):
    options, args = parse_options([Option()], validators=[destination_validator])

