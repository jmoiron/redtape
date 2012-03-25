redtape
-------

``redtape`` is a focused *document* generator that uses `github flavored markdown`_
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

To use, run ``rt`` on a document or directory full of documents.  If run on
a directory, ``rt`` will create html files for every markdown file (``.md``,
``.mdown``, or ``.markdown`` extensions)::

    > rt mydocument.md
    > rt documentation/

assets
------

By default, ``rt`` assumes you have set up a location to serve the files from
which have the assets that ``rt`` links into these documents.  The layout is
exactly the same as the `assets directory`_ in the redtape repository:
``/assets/{css,img,js}/..`` for each asset that you will be using.  If you want
to use redtape's default assets, you can easily create a suitable asset
directory in the current directory by running::

    > rt --create-assets

If you are running in single document mode or do not wish to set up an asset
directory on the eventual host for your HTML documents, you can tell redtape to
embed each asset used in a document by using ``--embed``::

    > rt --embed mydocument.md

.. _assets directory: https://github.com/jmoiron/redtape/blob/master/redtape/script.py

javascript
~~~~~~~~~~

By default, ``redtape`` not require any javascript to run, and will not embed
any in ``--embed`` mode.  If the ``--prettify`` option is selected, google's
prettify library will be used for source highlighting instead of `pygments`_,
and if ``--prettify`` and ``--embed`` are both used, it will be automatically
embedded.

Redtape is also suitable for simple single-page javascript demonstrations, and
if ``--use-js`` is enabled, redtape will include `jquery`_ and bootstrap's
javascript libraries.

.. _pygments: http://pygments.org
.. _jquery: http://jquery.org

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
