=====
rfcdl
=====

.. class:: center

**Always have a copy of your favorite `RFCs <https://www.ietf.org/standards/rfcs/>` in your pocket.**

rfcdl lets you download and synchronize RCFs in high-speed.

.. image:: https://img.shields.io/github/workflow/status/eikendev/rfcdl/Main
    :alt: Build status
    :target: https://github.com/eikendev/rfcdl/actions

.. image:: https://img.shields.io/pypi/status/rfcdl
    :alt: Development status
    :target: https://pypi.org/project/rfcdl/

.. image:: https://img.shields.io/pypi/l/rfcdl
    :alt: License
    :target: https://pypi.org/project/rfcdl/

.. image:: https://img.shields.io/pypi/pyversions/rfcdl
    :alt: Python version
    :target: https://pypi.org/project/rfcdl/

.. image:: https://img.shields.io/pypi/v/rfcdl
    :alt: Version
    :target: https://pypi.org/project/rfcdl/

.. image:: https://img.shields.io/pypi/dm/rfcdl
    :alt: Downloads
    :target: https://pypi.org/project/rfcdl/

Installation
============

From PyPI
---------

.. code:: bash

    pip install rfcdl

From Source
-----------

.. code:: bash

    ./setup.py install

Fedora
------

.. code:: bash

    sudo dnf copr enable eikendev/rfcdl
    sudo dnf install python3-rfcdl

Usage
=====

This tool can be used to download a large number of `RFC documents <https://www.ietf.org/standards/rfcs/>`_ in a short period of time.
I used it to keep a local mirror of all RFCs on my machines continuously synchronized.

For a quick introduction, let me show how you would use the tool to get started.

This is how you download the RFCs initially.

.. code:: bash

    rfcdl -d ~/download/rfc/

As can be seen above, you have to specify a directory where all RFC documents will be saved in.
Upon the next invocation of ``rfcdl``, only the RFCs missing in that directory will be downloaded.

This can then be combined with an alias that lets you read the local copy of any RFC.
The following command opens the RFC 8032 for me in less.

.. code:: bash

    rfc 8032

Check out `my dotfiles <https://github.com/eikendev/dotfiles/blob/199faa40873d8757a7c8f63d82d0f18a83b74ef9/source/zsh/function/rfc.zsh>`_ to see how this is implemented.

Arguments
=========

If you only want to download a random subset of all RFCs, use the ``--samples`` flag.
This can be used for testing.
For instance, the following will download 20 random RFC documents.

.. code:: bash

    rfcdl -d ~/download/rfc/ --samples 20

Since ``rfcdl`` downloads multiple files in parallel by default, one can specify how many simultaneous downloads are allowed using the ``--limit`` flag.
The following invocation will only download at most ten files in parallel.

.. code:: bash

    rfcdl -d ~/download/rfc/ --limit 10

To explicitly state how many times ``rfcdl`` should download a file upon error, the ``--retries`` flag can be used.
This can be useful in case one expects a bad connection.
This is how you could tell the tool to try to download each file at maximum five times.

.. code:: bash

    rfcdl -d ~/download/rfc/ --retries 5

Configuration
=============

A configuration file can be saved to ``~/.config/rfcdl/config.ini`` to avoid specifying the path for each invocation.
Of course, ``$XDG_CONFIG_HOME`` can be set to change your configuration path.
Alternatively, the path to the configuration file can be set via the ``--config-file`` argument.

.. code:: ini

    [GENERAL]
    RootDir = ~/download/rfc/

Development
===========

The source code is located on `GitHub <https://github.com/eikendev/rfcdl>`_.
To check out the repository, the following command can be used.

.. code:: bash

    git clone https://github.com/eikendev/rfcdl.git
