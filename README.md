pms
===
[![PyPI version](http://badge.fury.io/py/Poor-Mans-Spotify.png)](https://pypi.python.org/pypi/Poor-Mans-Spotify)
[![Downloads](https://pypip.in/d/Poor-Mans-Spotify/badge.png)](https://pypi.python.org/pypi/Poor-Mans-Spotify)


 - Search and stream music
 - Download music
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

then follow the interactive prompts, use `\h` to display help or you can
enter one of the following;

        \top for top tracks this week
        \top3m for top tracks of the last 3 months
        \top6m for top tracks of the last 6 months
        \topyear for top tracks of the last year
        \topall for all time top tracks
        \list <playlist_url> to load a playlist created on pleer.com


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


    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > 3

      -------------------------------
      Artist  : Richard Wagner
      Title   : Ride Of The Valkyries
      Length  : 10:07
      Bitrate : 128 Kb/s
      Size    : 9.274 Mb
      -------------------------------

   [<-] seek [->]
   [9] volume [0]
   [SPACE] pause / resume
   [q] stop
