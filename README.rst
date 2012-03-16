redtape
-------

``redtape`` is a focused documentation generator that uses `github flavored markdown`_
to generate simple, attractive HTML documents.  It automatically integrates with
`twitter bootstrap`_ and features simple, attractive styling.  It is inspired by
`d`_, but attempts to have a simple interface while still allowing users to style
and control their output documents to a high degree of customization.

.. _github flavored markdown: http://github.github.com/github-flavored-markdown/
.. _twitter bootstrap: http://twitter.github.com/bootstrap
.. _d: http://stevelosh.com/projects/d/

installing
----------

If you are on linux or OSX, you can use `pip`_ to install::

    > pip install redtape

Which will install redtape and its dependencies.

.. _pip: http://www.pip-installer.org/en/latest/index.html

usage
-----

To use, run ``rt`` on a document or directory full of documents.  It will
create html files for every markdown file (``.md``, ``.mdown``, or 
``.markdown`` extensions)::

    > rt mydocument.md
    > rt documentation/

By default, ``rt`` assumes you have set up a location to serve the files from
which have the assets that ``rt`` links into these documents.  If you can't be
bothered to do that, you have two options.  You can embed all of the assets
used in the resultant document::

    > rt --embed mydocument.md

You can ask ``rt`` to put a copy of its assets in a directory called
``./assets``::

    > rt --create-assets

You can run a simple HTTP server and look at them, fully styled::

    > python -m SimpleHTTPServer

customizing output
------------------

Customizing output is easy to do in a variety of ways.  Besides changing the
asset CSS for non-embedded documents, you can also add headers and footers or
even use custom document templates based on redtape's default template.

headers and footers
~~~~~~~~~~~~~~~~~~~

If you have a customized document header or footer you want added to your
documents, you can either add ``header.html`` and ``footer.html`` documents
to the base directory you are rendering or set default paths to be used 
in the config as ``header`` and ``footer``.  By default, these will be
placed at the top and bottom of your document, respectively.

A sample set of documents could be::

    > ls mydocs/
    mydocs/index.md       mydocs/simple.md      mydocs/advanced.md
    mydocs/header.html    mydocs/footer.html

Rendering mydocs with ``rt mydocs`` will use the header and footer for each
document in the directory.

custom templates
~~~~~~~~~~~~~~~~

If you have very specific requirements, you can write your own document
template and have total control of the output.  Redtape uses the `jinja2`_
templating engine, which is a widely used templating system similar to
django templates.  Run redtape with the ``--context`` argument to get a brief
idea of what variables are available to the template.

You can also inherit from ``basic.jinja``, which is the name of redtape's
default template.  This template defines two blocks, ``head`` and ``body``,
which would allow you to craft a distinct document body while, for instance,
retaining the basic CSS and JavaScript functionality of redtape.  Overriding
both will leave you with a standard HTML5 document structure.

You can specify a custom template to use with ``-t, --template`` or place
it in the document directory as ``custom.html`` or ``custom.jinja``.

.. _jinja2: http://jinja.pocoo.org/docs/
