#!/usr/bin/env python
# encoding: utf-8

"""
plan:
- types to check:
  - "object"
  - "any"
  - "sequence<..>"
  - promise
  -  "iterable", "maplike",?????
- What’s the difference between “optional” and the ?-prefix, e.g. look at line 18 and line 22.

- find all constructors and function calls that use those interesting types.

"""
import widlparser
from sys import argv
import re
import logging

logging.basicConfig(level=logging.DEBUG)
ENDC = '\033[0m'
UNDERLINE = '\033[4m'
PRE = UNDERLINE
POST = ENDC
re_cppcomments = ur"\/\*[\w\W\n\r]+\*\/[\n]*"
re_objectinsrc = ur"\b(object)\b"  # type: unicode


def normalize_idlsource(src):
    src = src.decode("utf-8")
    # replaces C-style /**/ comments, see https://regex101.com/r/TcvknN/1

    return re.sub(re_cppcomments, "", src, 0, re.MULTILINE)


custom_types = set()
object_types = []
whitelisted_types = ['EventHandler'] # ok to whitelist? discuss!

class CustomTypesMarker(object):
    def markupTypeName(self, text, construct):
        # oh wow, a type name that is "user-defined".
        custom_types.add(text)
        # TODO need to find out if that specific type is bad and scan for it. maybe re-do the webidl-scanning for
        # this whole construct and get alerted through another markupObjectType or is this overkill?

        return '', ''

class ObjectTypeMarker(object):
    def dbg(self, *args, **kwargs):
        print args
        # srcblock = str(construct.parent)
        # print construct.parent.idlType
        # print re.sub(re_objectinsrc, "{}object{}".format(PRE, POST), srcblock, 0, re.MULTILINE)

    def markupType(self, text, construct):
        # for all kinds of types. meh.
        if text in custom_types and text not in whitelisted_types:
            print "uh oh, not good", text, construct
            #self.dbg(text, construct)
        else:
            #print "skipping", text, construct
            pass
        return '', ''

    def markupObjectType(self, text, construct):
        #self.dbg(text, str(construct.name), construct.fullName)
        object_types.append({
            'name': construct.parent.name,  # PaymentMethodData
            'idltype': construct.parent.idlType,  # ...is a 'dictionary'
            'fieldname': construct.name,  # containing the field named 'data' of type object(always object)
            'fullname': construct.fullName,  # fullname is PaymentMethodData/data
            'badness': text  # type is "object"
        })
        return '', ''


FILE = open("PaymentRequest.webidl")  # open(argv[1], 'r')
idlsource = FILE.read()
idlsource = normalize_idlsource(idlsource)

widl = widlparser.parser.Parser(idlsource)
parser = widlparser.parser.Parser()
parser.parse(idlsource)
# this will learn us all custom types:
parser.markup(CustomTypesMarker())
# this will go through again and take them into consideration on top of objectish-things
parser.markup(ObjectTypeMarker())

import sys
sys.exit()

print "known objectish-types"
for ty in object_types:
    print ty

print "known custom types"
for ty in custom_types:
    print ty

# loop_through(widl.constructs)
