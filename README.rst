mps-youtube
===========

.. image:: http://badge.fury.io/py/mps-youtube.png
    :target: https://pypi.python.org/pypi/mps-youtube
.. image:: https://pypip.in/d/mps-youtube/badge.png
    :target: https://pypi.python.org/pypi/mps-youtube
.. image:: https://pypip.in/wheel/mps-youtube/badge.png
    :target: http://pythonwheels.com/
    :alt: Wheel Status


Features
--------
- Search and play audio/video from YouTube
- Search tracks of albums by album title
- Search and import YouTube playlists
- Create and save local playlists
- Download audio/video
- View video comments
- Works with Python 2.7+ and 3.x
- Works with Windows, Linux and Mac OS X 
- Requires mplayer or mpv

This project is based on `mps <https://github.com/np1/mps>`_, a terminal based program to search, stream and download music.  This implementation uses YouTube as a source of content and can play and download video as well as audio.  The `pafy <https://github.com/np1/pafy>`_ library handles interfacing with YouTube.

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

An album title can be specified and mps-youtube will attempt to find matches for
each track of the album, based on title and duration.  Type ``help search`` for
more info.


Customisation
~~~~~~~~~~~~~

.. image:: http://np1.github.io/mpsyt-images2/customisation.png

Search results can be customised to display additional fields and ordered
by various criteria.

This configuration was set up using the following commands::

    set max-results 50
    set console-width 130
    set columns user:14 date comments rating likes dislikes category:9
    set order views

Type ``help config`` for help on configuration options



Installation
------------

Using `pip <http://www.pip-installer.org>`_::
    
    [sudo] pip install mps-youtube

Mac OS X installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
Install mplayer with `MacPorts <http://www.macports.org>`_::

    sudo port install MPlayer


Windows installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the python `colorama <https://pypi.python.org/pypi/colorama>`_ module to get colors (optional)::

    pip install colorama

Download mplayer for your CPU type from the "Build Selection table" `here
<http://oss.netfarm.it/mplayer-win32.php>`_. 

Extract the mplayer.exe file, saving it to your mpsyt folder


Upgrading
---------

Upgrade pip installation::

    [sudo] pip install mps-youtube --upgrade

Usage
-----

mps-youtube is run on the command line using the command::
    
    mpsyt
    
Enter ``h`` from within the program for help.

