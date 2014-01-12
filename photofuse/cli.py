import sys

from optparse import OptionParser, Option

def validate_destination(options, args):
    if not options.destination:
        print "A destination is required"
        return False
    return True

def validate_source(options, args):
    if not options.source:
        print "A source is required"
        return False
    return True


def parse_options(options=[], validators=[], usage=None):
    validators.insert(0, validate_source)

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

def photofuse(argv=sys.argv):
    options, args = parse_options([Option()], validators=[destination_validator])

