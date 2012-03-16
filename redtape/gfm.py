"""GitHub flavoured markdown: because normal markdown has some vicious
gotchas.

Further reading on the gotchas:
http://blog.stackoverflow.com/2009/10/markdown-one-year-later/

This is a Python port of GitHub code, taken from
https://gist.github.com/901706

To run the tests, install nose ($ easy_install nose) then:

$ nosetests libs/gfm.py

Extended by Jason Moiron to add support for fenced blocks, fix a potential
bug in documents that mix pre and code blocks where they would not be
re-inserted into the document in the right order.

gfm now takes a kwarg "fenced" which can either be "pygments" or "bootstrap"
and will format the replacement text either with pygments or make it
easily available for twitter bootstrap's prettify integration.
"""

from uuid import uuid4
import re

def placeholder():
    return '{gfm-placeholder-%s}' % uuid4().hex

def remove_blocks(pattern, source):
    """Given a pattern and a source, replace all matching blocks with a
    placeholder and then return the updated source and blocks as a tuple."""
    blocks = {}
    match = pattern.search(source)
    while match:
        key = placeholder()
        original_block = match.group(0)
        blocks[key] = original_block
        source = pattern.sub(key, source, count=1)
        match = pattern.search(source)

    return source, blocks

def remove_fenced_blocks(source):
    """Replace fenced code blocks with placeholders."""
    pattern = re.compile(r'```.*?```', re.MULTILINE | re.DOTALL)
    return remove_blocks(pattern, source)

def remove_pre_blocks(source):
    """Replace <pre> blocks with placeholders"""
    pattern = re.compile(r'<pre>.*?</pre>', re.MULTILINE | re.DOTALL)
    return remove_blocks(pattern, source)

def remove_inline_code_blocks(source):
    """Replace inline code blocks with placeholders."""
    pattern = re.compile(r'`.*?`', re.DOTALL)
    return remove_blocks(pattern, source)

def get_lexer(lang, code):
    from pygments.lexers import get_lexer_by_name, guess_lexer
    fallback = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')
    if not lang:
        try: return guess_lexer(code)
        except: return fallback
    try: return get_lexer_by_name(lang, stripnl=True, encoding='UTF-8')
    except: return get_lexer(None, code)

def fenced_pygments(block):
    """Pygmentize a fenced block."""
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    pattern = re.compile(r'```(?P<lang>\w+)?(?P<code>.*?)```', re.MULTILINE|re.DOTALL)
    match = pattern.match(block)
    if not match:
        return block
    gd = match.groupdict()
    lang = gd.get('lang', None)
    code = gd.get('code', '').lstrip()
    cls = ('code %s' % lang) if lang else 'code'
    formatter = HtmlFormatter(linenos=True, cssclass=cls)
    lexer = get_lexer(lang, code)
    return highlight(code, lexer, formatter)

def fenced_bootstrap(block):
    """Set up a fenced block for bootstrap prettify highlighting."""
    pattern = re.compile(r'```(?P<lang>\w+)?(?P<code>.*?)```', re.MULTILINE|re.DOTALL)
    match = pattern.match(block)
    if not match:
        return block
    lang = match.groupdict().get('lang', None)
    code = match.groupdict().get('code', '')
    return '''<pre class="prettyprint linenums">%s</pre>''' % code

def gfm(text, fenced="bootstrap"):
    """Port of github's ruby github flavored markdown pre-processor, with
    added support for processing fenced blocks to be usable with bootstrap or
    to be straight-up highlighted with pygments."""
    text, fenced_blocks = remove_fenced_blocks(text)
    text, code_blocks = remove_pre_blocks(text)
    text, inline_blocks = remove_inline_code_blocks(text)

    if fenced and fenced in ("pygments", "bootstrap"):
        processor = fenced_pygments if fenced == "pygments" else fenced_bootstrap
        for key,block in fenced_blocks.items():
            fenced_blocks[key] = processor(block)

    # Prevent foo_bar_baz from ending up with an italic word in the middle.
    def italic_callback(matchobj):
        s = matchobj.group(0)
        # don't mess with URLs:
        if 'http:' in s or 'https:' in s:
            return s

        return s.replace('_', '\_')

    # fix italics for code blocks
    pattern = re.compile(r'^(?! {4}|\t).*\w+(?<!_)_\w+_\w[\w_]*', re.MULTILINE | re.UNICODE)
    text = re.sub(pattern, italic_callback, text)

    # linkify naked URLs
    regex_string = """
(^|\s) # start of string or has whitespace before it
(https?://[:/.?=&;a-zA-Z0-9_-]+) # the URL itself, http or https only
(\s|$) # trailing whitespace or end of string
"""
    pattern = re.compile(regex_string, re.VERBOSE | re.MULTILINE | re.UNICODE)

    # wrap the URL in brackets: http://foo -> [http://foo](http://foo)
    text = re.sub(pattern, r'\1[\2](\2)\3', text)

    # In very clear cases, let newlines become <br /> tags.
    def newline_callback(matchobj):
        if len(matchobj.group(1)) == 1:
            return matchobj.group(0).rstrip() + '  \n'
        else:
            return matchobj.group(0)

    pattern = re.compile(r'^[\w\<][^\n]*(\n+)', re.MULTILINE | re.UNICODE)
    text = re.sub(pattern, newline_callback, text)

    # now restore removed code blocks
    removed_blocks = {}
    removed_blocks.update(fenced_blocks)
    removed_blocks.update(code_blocks)
    removed_blocks.update(inline_blocks)

    for placeholder,removed_block in removed_blocks.iteritems():
        text = text.replace(placeholder, removed_block, 1)

    return text

def gfmd(text, fenced="bootstrap"):
    """Run github-flavored markdown on text."""
    from markdown import markdown
    return markdown(gfm(text, fenced))

# Test suite.
try:
    from nose.tools import assert_equal
except ImportError:
    def assert_equal(a, b):
        assert a == b, '%r != %r' % (a, b)

def test_single_underscores():
    """Don't touch single underscores inside words."""
    assert_equal(
        gfm('foo_bar'),
        'foo_bar',
    )

def test_underscores_code_blocks():
    """Don't touch underscores in code blocks."""
    assert_equal(
        gfm('    foo_bar_baz'),
        '    foo_bar_baz',
    )

def test_underscores_inline_code_blocks():
    """Don't touch underscores in code blocks."""
    assert_equal(
        gfm('foo `foo_bar_baz`'),
        'foo `foo_bar_baz`',
    )

def test_underscores_pre_blocks():
    """Don't touch underscores in pre blocks."""
    assert_equal(
        gfm('<pre>\nfoo_bar_baz\n</pre>'),
        '<pre>\nfoo_bar_baz\n</pre>',
    )

def test_pre_block_pre_text():
    """Don't treat pre blocks with pre-text differently."""
    a = '\n\n<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    b = 'hmm<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    assert_equal(
        gfm(a)[2:],
        gfm(b)[3:],
    )

def test_two_underscores():
    """Escape two or more underscores inside words."""
    assert_equal(
        gfm('foo_bar_baz'),
        'foo\\_bar\\_baz',
    )
    assert_equal(
        gfm('something else then foo_bar_baz'),
        'something else then foo\\_bar\\_baz',
    )

def test_newlines_simple():
    """Turn newlines into br tags in simple cases."""
    assert_equal(
        gfm('foo\nbar'),
        'foo  \nbar',
    )

def test_newlines_group():
    """Convert newlines in all groups."""
    assert_equal(
        gfm('apple\npear\norange\n\nruby\npython\nerlang'),
        'apple  \npear  \norange\n\nruby  \npython  \nerlang',
    )

def test_newlines_long_group():
    """Convert newlines in even long groups."""
    assert_equal(
        gfm('apple\npear\norange\nbanana\n\nruby\npython\nerlang'),
        'apple  \npear  \norange  \nbanana\n\nruby  \npython  \nerlang',
    )

def test_newlines_list():
    """Don't convert newlines in lists."""
    assert_equal(
        gfm('# foo\n# bar'),
        '# foo\n# bar',
    )
    assert_equal(
        gfm('* foo\n* bar'),
        '* foo\n* bar',
    )

def test_underscores_urls():
    """Don't replace underscores in URLs"""
    assert_equal(
        gfm('[foo](http://example.com/a_b_c)'),
        '[foo](http://example.com/a_b_c)'
        )

def test_underscores_in_html():
    """Don't replace underscores in HTML blocks"""
    assert_equal(
        gfm('<img src="http://example.com/a_b_c" />'),
        '<img src="http://example.com/a_b_c" />'
        )

def test_linkify_naked_urls():
    """Wrap naked URLs in []() so they become clickable links."""
    assert_equal(
        gfm(" http://www.example.com:80/foo?bar=bar&biz=biz"),
        " [http://www.example.com:80/foo?bar=bar&biz=biz](http://www.example.com:80/foo?bar=bar&biz=biz)"
        )
