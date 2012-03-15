#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""rt (redtape) is a simple, no-nonsense documentation generator which will
convert one or more markdown documents into good looking HTML files with
niceties like syntax highlighting, simple access to icons and styles from
twitter bootstrap, and more.

It is not meant for complex documentation generation, but as an easy
way to flexibly create one-off documents or collections of documents while
retaining control over document style."""

import pygments
import jinja2
try:
    from lxml.html import fragment_fromstring
    from lxml.cssselect import CSSSelector as cs
    has_lxml = True
except:
    has_lxml = False

import os
import redtape
from glob import glob
from redtape import gfm
from optparse import OptionParser

parser = OptionParser(version=".".join(map(str, redtape.VERSION)),
        usage="%prog [opts] <file(s)>")
parser.add_option("-t", "--template", help="use alternate document template")
parser.add_option("-e", "--embed", action="store_true", help="embed all css/js in each output file")
parser.add_option("", "--pygments", action="store_true", help="use pygments for code blocks")
parser.add_option("", "--pygments-class", help="use alternate pygments class (implies --pygments)")

asset_path = os.path.join(os.path.dirname(__file__), "assets")

def extract_title(fragment):
    if not has_lxml: return ""
    doc = fragment_fromstring(fragment)
    try:
        return cs('h1')(doc).text_content
    except:
        import traceback
        traceback.print_exc()
        return ""


def markdown_files(directory):
    paths = []
    for ext in (".md", ".mdown", ".markdown"):
        paths += glob(os.path.join(directory, "*%s" % ext))
    return paths

def args_to_paths(args):
    paths = []
    for arg in args:
        if not os.path.exists(arg):
            raise Exception("File not found: %s" % arg)
        if os.path.isfile(arg):
            paths.append(arg)
        if os.path.isdir(arg):
            paths += markdown_files(arg)
    return paths

def main():
    opts, args = parser.parse_args()
    if not args:
        parser.print_usage()
        return -1

    use_prettify = not opts.pygments

    css = [
        "assets/css/bootstrap.min.css",
        "assets/css/%s" % ("prettify.css" if use_prettify else "pygments.css"),
    ]
    js = [
        "assets/js/jquery.min.js",
        "assets/js/prettify.js",
        "assets/js/bootstrap.min.js",
    ]

    paths = args_to_paths(args)
    for path in paths:
        output = path.rsplit('.', 1)[0] + '.html'
        with open(path) as f:
            document = gfm.gfmd(f.read())
        title = extract_title(document)
        print document
