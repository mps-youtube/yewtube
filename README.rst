pms
===

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
- Works with Windows, Linux and Mac OSX 10.9
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


Mac OSX installation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~
    
Download mplayer::

    https://www.macupdate.com/app/mac/18580/mplayer

Make a link for mplayer::

    ln -s /Applications/MPlayer OSX.app/Contents/Resources/External_Binaries/mplayer.app/Contents/MacOS/mplayer /usr/local/bin/mplayer

Install X11::

    http://xquartz.macosforge.org/landing/
    
if using MplayerX::

    ln -s /Applications/MPlayerX.app/Contents/Resources/binaries/x86_64/mplayer /usr/local/bin/mplayer

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
    
Enter `h` from within the program for help.

Searching
~~~~~~~~~

You can enter an artist/song name to search whenever the program is expecting
text input. Searches must be prefixed with a . (dot) character.

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
new playlist will be created if it doesn't already exist.

``ls`` to list your saved playlists

``open <playlist_name>`` to open a saved playlist as the current playlist

``vp`` to view the current playlist (then use rm, mv and sw to modify it)

``save <playlist_name>`` to save the currently displayed songs as a stored
playlist on disk

``rm <playlist_name>`` to delete a playlist from disk

You can load a playlist when invoking pms using the following command:

    ``pms open <playlistname>``

``q`` to quit

``h`` for help



Other Commands
--------------

``top`` show top tracks this week

``top3m`` show top tracks for last 3 months

``top6m`` show top tracks for last 6 months

``topyear`` show top tracks for last year

``topall`` show all time top tracks
