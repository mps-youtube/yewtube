pms
===
[![PyPI version](http://badge.fury.io/py/Poor-Mans-Spotify.png)](https://pypi.python.org/pypi/Poor-Mans-Spotify)
[![Downloads](https://pypip.in/d/Poor-Mans-Spotify/badge.png)](https://pypi.python.org/pypi/Poor-Mans-Spotify)


 - Search and stream music
 - Download music
 - Create playlists
 - Works with Python 2.7 and 3.x
 - Works with Windows, Linux and Mac OSX 10.9
 - No Python dependencies
 - Requires mplayer

# Installation

### Using pip:
    
    sudo pip install Poor-Mans-Spotify

### Using git:

    git clone https://github.com/np1/pms.git
    
###Manually:

Download [zip](https://github.com/np1/pms/archive/master.zip)/[tar.gz](https://github.com/np1/pms/archive/master.tar.gz) file and extract

### Mac OSX installation notes:
    
Download mplayer

    https://www.macupdate.com/app/mac/18580/mplayer

Make a link for mplayer

    ln -s /Applications/MPlayer OSX.app/Contents/Resources/External_Binaries/mplayer.app/Contents/MacOS/mplayer /usr/local/bin/mplayer

Install X11

    http://xquartz.macosforge.org/landing/
    
if using MplayerX: 

    ln -s /Applications/MPlayerX.app/Contents/Resources/binaries/x86_64/mplayer /usr/local/bin/mplayer# Upgrade

# Upgrading

It is recommended you update to the latest version

### Upgrade pip installation:

    sudo pip install Poor-Mans-Spotify --upgrade

### Upgrade git clone:

from within the pms directory;

    git pull


# Usage

    usage: pms query [query ...]

or simply:

    pms

You can enter an artist / song name to search at any time the program is
running.

Any time you have a list of songs displayed (except during playback), you can
use the following functions:

```all``` to play all
```1,2,3``` to play songs 1 2 and 3
```2-4, 6, 6-3``` to play songs 2, 3, 4, 6, 6, 5, 4, 3

```d 4``` to download song number 4

```rm 1,3``` to remove songs 1, 2 and 3.  Or use ```rm 1,2,5-7``` to remove a range

```rm all``` to remove all songs

```sw 1,3``` to swap the position of songs 1 and 3

```mv 1,3``` to move song 1 to postion 3

```add 1,2,3``` to add songs 1,2 and 3 to the temporary playlist.  Or use 

```add 1,2,5-7``` to add a range.

```vp``` to view the temp playlist (then rm, mv and sw to modify it)

```save <playlist_name>``` to save the currently displayed songs as a stored
playlist on disk

```lp``` to view saved playlists

```open <playlist_name>``` to open a saved playlist as the current playlist

```rm <playlist_name>``` to remove a playlist from disk

If you remember the name of a playlist, you can call it when starting pms by
entering at the command prompt:

```pms open <playlistname>```

```q to quit```
```h for help```

Have fun!  There is still much work to be done like tidier string formatting,
context-sensetive help and there are probably still plenty of bugs although 
it's perfectly usable.  Keep checking back for updates.

# Screenshot
![pms running in terminal](http://i.imgur.com/Oqyz5vk.png "pms running in terminal")

# Usage Example:

    $ > ./pms

    Enter artist/song name or \h for help or \q to quit: wagner

    Searching for 'wagner'

    Item   Size    Artist                Track                  Length   Bitrate 
    1      2.1 Mb  Wilhelm Richard Wagn  Die Hochzeit (Сон в л  03:09    96      
    2      7.2 Mb  Wilhelm Richard Wagn  Ein Sommernachtstraum  03:09    320     
    3      9.2 Mb  Richard Wagner        Ride Of The Valkyries  10:07    128     
    4      5.6 Mb  Wilhelm Richard Wagn  Der Weg In Walghal     04:05    192     
    5      3.2 Mb  Wilhelm Richard Wagn  Die Hochze             02:20    192     
    6      4.8 Mb  Richard Wagner        Carmina Burana         05:19    128     
    7      4.8 Mb  Wagner                O Fortuna (Excalibur   05:18    128     
    8      3.5 Mb  Wilhelm Richard Wagn  Das Leben (Жизнь)      03:55    128     
    9      10. Mb  Johann Sebastian Bac  Concerto in D minor a  04:47    320     
    10     9.2 Mb  Richard Wagner        Die Walküre (Der Ring  10:07    128     
    11     3.4 Mb  Wilhelm Richard Wagn  Spring waltz           01:31    320     
    12     2.1 Mb  Wilhelm Richard Wagn  Die Hochzeit (Der Tra  03:09    96      
    13     9.8 Mb  Richard Wagner (Виль  The Mastersinger of N  10:42    128     
    14     3.2 Mb  Wilhelm Richard Wagn  Die Hochzeit           02:20    192     
    15     10. Mb  Richard Wagner        Tristan and Isolde     11:45    128     
    16     3.5 Mb  Wagner Riñhard        Вальс I. Жизнь         03:55    128     
    17     3.1 Mb  Wilhelm Richard Wagn  Tear                   03:27    128     
    18     5.6 Mb  Wilhelm Richard Wagn  Requem for a dream     04:05    192     
    19     3.8 Mb  Richard Wagner Lisa   Now we are free        04:14    128     
    20     8.8 Mb  Wilhelm Richard Wagn  Der Weg in Walghal     06:28    192     

