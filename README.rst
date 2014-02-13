mps-youtube
===========

.. image:: http://badge.fury.io/py/mps-youtube.png
    :target: https://pypi.python.org/pypi/mps-youtube
.. image:: https://pypip.in/d/mps-youtube/badge.png
    :target: https://pypi.python.org/pypi/mps-youtube


Features
--------
- Search and play audio/video
- Create local playlists
- Download audio/video
- Works with Python 2.7 and 3.x
- Works with Windows, Linux and Mac OS X 
- Requires mplayer

This project is based on `mps <https://github.com/np1/mps>`_, which is a terminal based program
to search, stream and download music.  This implementation uses YouTube as a 
source of content and can play and download video as well as audio.  The `pafy <https://github.com/np1/pafy>`_
library handles interfacing with YouTube.

Installation
------------

Using `pip <http://www.pip-installer.org>`_::
    
    sudo pip install mps-youtube

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

It is recommended you update to the latest version.

Upgrade pip installation::

    sudo pip install mps-youtube --upgrade

Usage
-----

mps-youtube is run on the command line using the command::
    
    mpsyt
    
Enter ``h`` from within the program for help.

Searching
~~~~~~~~~

You can enter an search term name to search whenever the program is expecting
text input. Searches must be prefixed with either a . or / character.

Enter ``n`` or ``p`` to go to the next / previous page of results

When a list of items is displayed, such as search results or a playlist, you
can use the following commands:

Information
~~~~~~~~~~~

``i 3`` to view info on item 3

Downloading
~~~~~~~~~~~

``d 3`` to download item 3 (will open new menu)
``da 3`` to download audio stream of item 3
``dv 3`` to download video stream of item 3

Playback
~~~~~~~~

``all`` to play all displayed items

``1,2,3`` to play items 1 2 and 3

``2-4,6,6-3`` to play items 2, 3, 4, 6, 6, 5, 4, 3

Note: The commands ``shuffle`` and ``repeat`` can be inserted at the start or
end of any of the above to enable those play modes: eg, ``shuffle 1-4`` or
``2-4,1 repeat`` 

Editing
~~~~~~~
``rm 1,5`` to remove items 1 and 5.

``rm 1,2,5-7`` to remove items 1,2 and 5-7.

``rm all`` to remove all items

``sw 1,3`` to swap the position of items 1 and 3

``mv 1,3`` to move items 1 to postion 3

Playlist commands
~~~~~~~~~~~~~~~~~

``add 1,2,3`` to add items 1,2 and 3 to the current playlist. 

``add 1-4,6,8-10`` to add items 1-4, 6, and 8-10 to the current playlist
    
``add 1-4,7 <playlist_name>`` to add items 1-4 and 7 to a saved playlist.  A
new playlist will be created if the given name doesn't already exist.

``vp`` to view the current playlist (then use rm, mv and sw to modify it)

``ls`` to list your saved playlists

``open <playlist_name or ID>`` to open a saved playlist as the current playlist 

``view <playlist_name or ID>`` to view a playlist (leaves current playlist intact)

``play <playlist_name or ID>`` to play a saved playlist directly.

``save`` or ``save <playlist_name>`` to save the currently displayed items as a
stored playlist on disk

``rmp <playlist_name or ID>`` to delete a playlist from disk

``mv <old_name or ID> <new_name>`` to rename a playlist

``q`` to quit

``h`` for help


Advanced Tips
-------------

Playlist Name Completion
~~~~~~~~~~~~~~~~~~~~~~~~

When using ``open``, ``view`` or ``play``  to access a playlist, you can enter
the first few characters instead of the whole name.  The first alphabetically
matching playlist will be opened / displayed.

Invocation
~~~~~~~~~~

To play a saved playlist when invoking mps-youtube use the following command:

    ``mpsyt play <playlistname>``

This also works for other commands, eg:

    ``mpsyt .mozart`` to search 

    ``mpsyt view <playlistname>`` to view a saved playlist

    ``mpsyt ls`` to list saved playlists

    ``mpsyt open moz`` to open a saved playlist called mozart.

Specifying Ranges
~~~~~~~~~~~~~~~~~

When selecting items for playback, removing or adding you can use ``5-`` to 
select items 5 upward and ``-5`` to select up to item 5.  This can be included
with other choices so for example: ``5,3,7-,-2``.  You can also use spaces
instead of commas eg. ``5 3 7- -2``.

Changing Player Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set a different player, from within mps-youtube::

    set player mpv

or::

    set player mplayer

Other Configuration
~~~~~~~~~~~~~~~~~~~

To view configuration, enter ``set`` and to change any item enter: 
``set <item> <value>``.  This can be used to change the download path (DDIR)
and will persist after exiting the program.  To reset all settings to default,
use ``set all default`` or for a single item, ``set <item> default``

Search All Categories
~~~~~~~~~~~~~~~~~~~~~

To search all YouTube categories (instead of just music), enter:: 
    
    set search_music false

List YouTube User Uploads
~~~~~~~~~~~~~~~~~~~~~~~~~

To list the uploaded videos of a YouTube user:

    /username -user

Show Video Content / Fullscreen Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To view and download video instead of audio, enter::

    set show_video true

To play video content in fullscreen mode::

    set fullscreen true
