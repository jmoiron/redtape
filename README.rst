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

