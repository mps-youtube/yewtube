mps-youtube
===========

.. image:: https://img.shields.io/pypi/v/mps-youtube.svg
    :target: https://pypi.python.org/pypi/mps-youtube
.. image:: https://img.shields.io/pypi/dm/mps-youtube.svg
    :target: https://pypi.python.org/pypi/mps-youtube
.. image:: https://img.shields.io/pypi/wheel/mps-youtube.svg
    :target: http://pythonwheels.com/
    :alt: Wheel Status


Features
--------
- Search and play audio/video from YouTube
- Search tracks of albums by album title
- Search and import YouTube playlists
- Create and save local playlists
- Download audio/video
- Convert to mp3 & other formats (requires ffmpeg or avconv)
- View video comments
- Works with Python 3.x
- Works with Windows, Linux and Mac OS X 
- Requires mplayer or mpv

This project is based on `mps <https://github.com/np1/mps>`_, a terminal based program to search, stream and download music.  This implementation uses YouTube as a source of content and can play and download video as well as audio.  The `pafy <https://github.com/np1/pafy>`_ library handles interfacing with YouTube.

`FAQ / Troubleshooting common issues <https://github.com/np1/mps-youtube/wiki/Troubleshooting>`_

Screenshots
-----------


Search
~~~~~~
.. image:: http://np1.github.io/mpsyt-images2/std-search.png

A standard search is performed by entering ``/`` followed by search terms.

Local Playlists
~~~~~~~~~~~~~~~
.. image:: http://np1.github.io/mpsyt-images2/local-playlists.png

Search result items can easily be stored in local playlists.

YouTube Playlists
~~~~~~~~~~~~~~~~~
.. image:: http://np1.github.io/mpsyt-images2/playlist-search.png

YouTube playlists can be searched and played or saved as local playlists.

Download
~~~~~~~~
.. image:: http://np1.github.io/mpsyt-images2/download.png

Content can be downloaded in various formats and resolutions.

Comments
~~~~~~~~
.. image:: http://np1.github.io/mpsyt-images2/comments.png

A basic comments browser is available to view YouTube user comments.

Music Album Matching
~~~~~~~~~~~~~~~~~~~~

.. image:: http://np1.github.io/mpsyt-images2/album-1.png

.. image:: http://np1.github.io/mpsyt-images2/album-2.png

An album title can be specified and mps-youtube will attempt to find matches for each track of the album, based on title and duration.  Type ``help search`` for more info.  

Customisation
~~~~~~~~~~~~~

.. image:: http://np1.github.io/mpsyt-images2/customisation2.png

Search results can be customised to display additional fields and ordered by various criteria.

This configuration was set up using the following commands::

    set order views
    set columns user:14 date comments rating likes dislikes category:9 views

Type ``help config`` for help on configuration options



Installation
------------

Using `pip <http://www.pip-installer.org>`_::
    
    [sudo] pip3 install mps-youtube

Additional Mac OS X installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
Install mplayer with `MacPorts <http://www.macports.org>`_::

    sudo port install MPlayer

Or with `Homebrew <http://brew.sh>`_::

    brew install mplayer

Additional Windows installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As an alternative to installing with pip, there is a standalone binary available. Go to `Releases <https://github.com/np1/mps-youtube/releases>`_ and download mpsyt-VERSION.exe under downloads for the latest release.

Install the python `colorama <https://pypi.python.org/pypi/colorama>`_ module to get colors (optional)::

    pip3 install colorama

Download mplayer for your CPU type from the "Build Selection table" `here <http://oss.netfarm.it/mplayer-win32.php>`_.

Extract the ``mplayer.exe`` file, saving it to the folder that ``mpsyt.exe`` resides in (usually ``C:\PythonXX\Scripts\``) or to a folder in the system path.

Alternatively to mplayer, use ``mpv.exe`` which can be downloaded from: http://mpv.io/installation/

Run via Docker container
~~~~~~~~~~~~~~~~~~~~~~~~

Using `Docker <http://www.docker.com>`_, run with::

    sudo docker run -v /dev/snd:/dev/snd -it --rm --privileged --name mpsyt mpsyt

Additional Docker notes
~~~~~~~~~~~~~~~~~~~~~~~

If you would like to locally build the container you can run the following steps

Check out this repo::

    git clone https://github.com/np1/mps-youtube.git

Enter the directory and run docker build::

    cd mps-youtube
    sudo docker build -t mpsyt .

Now run the container interactively with::

    sudo docker run -v /dev/snd:/dev/snd -it --rm --privileged --name mpsyt mpsyt

In order to have access to the local sound device (/dev/snd) the container needs to be privileged.

Upgrading
---------

Upgrade pip installation::

    [sudo] pip3 install mps-youtube --upgrade

Usage
-----

mps-youtube is run on the command line using the command::
    
    mpsyt
    
Enter ``h`` from within the program for help.

IRC
---

An IRC channel `#mps-youtube` for the project is available on Freenode (chat.freenode.net:6697).
