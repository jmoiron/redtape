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
    from lxml.html import document_fromstring
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
parser.add_option("-d", "--destination", help="write HTML/assets to a separate destination directory")
parser.add_option("", "--use-js", action="store_true", help="link in jquery & bootstrap js files")
parser.add_option("", "--create-assets", action="store_true", help="create/update directory ./assets with rt assets")
parser.add_option("", "--pygments", action="store_true", help="use pygments for code blocks instead of hilite")

pkg_dir = os.path.dirname(__file__)
asset_path = os.path.join(os.path.dirname(__file__), "assets")

def extract_title(fragment):
    if not has_lxml: return ""
    doc = document_fromstring(fragment)
    try:
        return cs('h1')(doc)[0].text_content()
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

def create_assets():
    current = os.curdir()
    destination = os.path.join(current, "assets")
    if os.path.exists(destination) and not os.path.isdir(destination):
        raise Exception("The path ./assets exists and is a file.")

def find_custom_template(args):
    """Finds a custom template in the directories provided as arguments.  The
    first template found is returned and used for the remainder of the docs."""
    for arg in args:
        if os.path.isdir(arg):
            dirlist = os.listdir(arg)
            if "custom.html" in dirlist:
                return os.path.join(arg, "custom.html")
            elif "custom.jinja" in dirlist:
                return os.path.join(arg, "custom.jinja")

def get_jinja_template(opts, args):
    """Get a jinja template suitable for rendering our documents.  Care is
    taken to chose figure out which template to render, and to allow custom
    templates to inherit from the default one."""
    template_paths = [asset_path]
    template = "basic.jinja"
    if opts.template:
        extra, template = os.path.split(os.path.abspath(opts.template))
        template_paths.append(extra)
    else:
        template = find_custom_template(args) or template

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_paths))
    return env.get_template(template)

def main():
    opts, args = parser.parse_args()
    if not args:
        parser.print_usage()
        return -1

    if opts.create_assets:
        create_assets()
        return 0


    context = {}
    use_prettify = context['prettify'] = not opts.pygments

    css = [
        "assets/css/bootstrap.min.css",
        "assets/css/%s" % ("prettify.css" if use_prettify else "pygments.css"),
    ]
    js = [] if not opts.use_js else [
        "assets/js/jquery.min.js",
        "assets/js/bootstrap.min.js",
    ]

    if use_prettify: # if prettifying, link prettify no matter what
        js.append("assets/js/prettify.js")

    context['js'] = js
    context['css'] = css

    if opts.embed:
        embed = {'css':[], 'js':[]}
        for csf in css:
            with open(os.path.join(pkg_dir, csf)) as f:
                embed['css'].append(f.read().decode("utf-8"))
        for jsf in js:
            with open(os.path.join(pkg_dir, jsf)) as f:
                embed['js'].append(f.read().decode("utf-8"))
        context['embed'] = embed


    paths = args_to_paths(args)
    for path in paths:
        output = path.rsplit('.', 1)[0] + '.html'
        with open(path) as f:
            document = gfm.gfmd(f.read(), fenced="pygments" if opts.pygments else "bootstrap")
        context['title'] = extract_title(document)
        context['document'] = document
        template = get_jinja_template(opts, args)
        print template.render(context).encode("utf-8")

