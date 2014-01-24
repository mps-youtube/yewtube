pms
===
version 0.18.34

.. image:: http://badge.fury.io/py/Poor-Mans-Spotify.png
    :target: https://pypi.python.org/pypi/Poor-Mans-Spotify
.. image:: https://pypip.in/d/Poor-Mans-Spotify/badge.png
    :target: https://pypi.python.org/pypi/Poor-Mans-Spotify

Features
--------
- Search and stream music
- Create playlists
- Download music
- Works with Python 2.7 and 3.x
- Works with Windows, Linux and Mac OS X 
- No Python dependencies
- Requires mplayer

Screenshots
-----------

Search
~~~~~~

.. image:: http://i.imgur.com/SnqxqZz.png

Playback
~~~~~~~~

.. image:: http://i.imgur.com/3sYlktI.png

.. image:: http://i.imgur.com/yzgQBmx.png

Playlists
~~~~~~~~~

.. image:: http://i.imgur.com/RDEXLPW.png



Installation
------------

Using pip::
    
    sudo pip install Poor-Mans-Spotify

Using git::

    git clone https://github.com/np1/pms.git
   
Manually::

    Download zip file or tar.gz and extract:

    https://github.com/np1/pms/archive/master.zip

    https://github.com/np1/pms/archive/master.tar.gz


Mac OS X installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
Install mplayer with MacPorts::

    sudo port install MPlayer


Windows installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the python `colorama <https://pypi.python.org/pypi/colorama>`_ module to get colors::

    pip install colorama


Upgrading
---------

It is recommended you update to the latest version.

Upgrade pip installation::

    sudo pip install Poor-Mans-Spotify --upgrade

Upgrade git clone::

    (from within the pms directory)

    git pull

Usage
-----

pms is run on the command line using the command::
    
    pms
    
or on Linux/MacOS if you are in the same directory::

    ./pms
    
Enter ``h`` from within the program for help.

Searching
~~~~~~~~~

You can enter an artist/song name to search whenever the program is expecting
text input. Searches must be prefixed with a . (dot) character.

Enter ``n`` or ``p`` to go to the next / previous page of results

When a list of songs is displayed, such as search results or a playlist, you
can use the following commands:

Downloading
~~~~~~~~~~~
``d 3`` to download song 3

Playback
~~~~~~~~

``all`` to play all displayed tracks

``1,2,3`` to play songs 1 2 and 3

``2-4,6,6-3`` to play songs 2, 3, 4, 6, 6, 5, 4, 3

Note: The commands ``shuffle`` and ``repeat`` can be inserted at the start or
end of any of the above to enable those play modes: eg, ``shuffle 1-4`` or
``2-4,1 repeat`` 

Editing
~~~~~~~
``rm 1,5`` to remove songs 1 and 5.

``rm 1,2,5-7`` to remove songs 1,2 and 5-7.

``rm all`` to remove all songs

``sw 1,3`` to swap the position of songs 1 and 3

``mv 1,3`` to move song 1 to postion 3

Playlist commands
~~~~~~~~~~~~~~~~~

``add 1,2,3`` to add songs 1,2 and 3 to the current playlist. 

``add 1-4,6,8-10`` to add songs 1-4, 6, and 8-10 to the current playlist
    
``add 1-4,7 <playlist_name>`` to add songs 1-4 and 7 to a saved playlist.  A
new playlist will be created if the given name doesn't already exist.

``vp`` to view the current playlist (then use rm, mv and sw to modify it)

``ls`` to list your saved playlists

``open <playlist_name or ID>`` to open a saved playlist as the current playlist 

``view <playlist_name or ID>`` to view a playlist (leaves current playlist intact)

``play <playlist_name or ID>`` to play a saved playlist directly.

``save`` or ``save <playlist_name>`` to save the currently displayed songs as a
stored playlist on disk

``rmp <playlist_name or ID>`` to delete a playlist from disk

``mv <old_name or ID> <new_name>`` to rename a playlist

``q`` to quit

``h`` for help

Other Commands
--------------

``top`` show top tracks this week

``top3m`` show top tracks for last 3 months

``top6m`` show top tracks for last 6 months

``topyear`` show top tracks for last year

``topall`` show all time top tracks

``list [pleer playlist url]``` to import a playlist from the web.

Advanced Tips
-------------

Playlist Name Completion
~~~~~~~~~~~~~~~~~~~~~~~~

When using ``open``, ``view`` or ``play``  to access a playlist, you can enter
the first few characters instead of the whole name.  The first alphabetically
matching playlist will be opened / displayed.

Invocation
~~~~~~~~~~

To play a saved playlist when invoking pms use the following command:

    ``pms play <playlistname>``

This also works for other commands, eg:

    ``pms .mozart`` to search 

    ``pms view <playlistname>`` to view a saved playlist

    ``pms ls`` to list saved playlists

    ``pms top`` to list top tracks this week

    ``pms open moz`` to open a saved playlist called mozart.

Specifying Ranges
~~~~~~~~~~~~~~~~~

When selecting songs for playback, removing or adding you can use ``5-`` to 
select song 5 upward and ``-5`` to select up to song 5.  This can be included
with other choice so for example: ``5,3,7-,-2``.  You can also use spaces
instead of commas eg. ``5 3 7- -2`` or a combination of both eg. ``3,4 7-9, 1``

Quality / Bitrate
~~~~~~~~~~~~~~~~~

Add ``+best`` to a search query to return high bitrate results or ``+good`` to
exclude them.

Other Configuration
~~~~~~~~~~~~~~~~~~~

To view configuration, enter ``showconfig`` and to change any item enter: 
``set <item> "value"``.  This can be used to change the download path (DDIR)
and will persist after exiting the program.  To reset all settings to default,
use ``set all "default"`` or for a single item, ``set <item> "default"``
