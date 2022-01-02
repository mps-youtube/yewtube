yewtube
===========
![](https://img.shields.io/pypi/v/mps-youtube.svg) ![](https://img.shields.io/pypi/dm/mps-youtube.svg)  ![](https://img.shields.io/pypi/wheel/mps-youtube.svg)

Installation
------------
1. It is recommended that you first Uninstall previous installations of **_mps-youtube_** .i.e. `pip uninstall mps-youtube`
2.  Install **_pipx_** using `pip install pipx`
3.  Install `yewtube` using `pipx install git+https://github.com/iamtalhaasghar/yewtube.git`
4.  Install latest pafy version using 
 ```
pipx runpip yewtube uninstall pafy
pipx runpip yewtube install git+https://github.com/mps-youtube/pafy 
```
5.  Now, type `yt` That's it.

Features
--------

-   Search and play audio/video from YouTube
-   Search tracks of albums by album title
-   Search and import YouTube playlists
-   Create and save local playlists
-   Download audio/video
-   Convert to mp3 & other formats (requires ffmpeg or avconv)
-   View video comments
-   Works with Python 3.x
-   Works with Windows, Linux and Mac OS X
-   Requires mplayer, mpv or VLC
-   Run audio in VLC with no GUI

This project is based on [mps-youtube](https://github.com/mps-youtube/mps-youtube) and mps-youtube is based on [mps](https://web.archive.org/web/20180429034221/https://github.com/np1/mps), a terminal based program to search, stream and download music. This
implementation uses YouTube as a source of content and can play and
download video as well as audio. The [pafy](https://github.com/mps-youtube/pafy)  library handles interfacing with YouTube.

[mps-youtube wiki](https://github.com/mps-youtube/mps-youtube/wiki/Troubleshooting) <br>
[yewtube wiki](https://github.com/iamtalhaasghar/yewtube/wiki/FAQ)

Screenshots
-----------

Search:<br>
![](http://mps-youtube.github.io/mps-youtube/std-search.png)

A standard search is performed by entering `/` followed by search terms.

You can play all of the search results by giving `1-` as input

Repeating song/songs can be done with `song_number[loop]`, for example:
`1[3]` or `4-6[2]`

Local Playlists:<br>
![](http://mps-youtube.github.io/mps-youtube/local-playlist.png)

Search result items can easily be stored in local playlists.

YouTube Playlists:<br>
![](http://mps-youtube.github.io/mps-youtube/playlist-search.png)

YouTube playlists can be searched and played or saved as local
playlists.

A playlist search is performed by `//` followed by search term.

Download:<br>
![](http://mps-youtube.github.io/mps-youtube/download.png)

Content can be downloaded in various formats and resolutions.

Comments:<br>
![](http://mps-youtube.github.io/mps-youtube/comments.png)

A basic comments browser is available to view YouTube user comments.

Music Album Matching:<br>

![](http://mps-youtube.github.io/mps-youtube/album-1.png)

![](http://mps-youtube.github.io/mps-youtube/album-2.png)

An album title can be specified and yewtube will attempt to find
matches for each track of the album, based on title and duration. Type
`help search` for more info.

Customisation:<br>

![](http://mps-youtube.github.io/mps-youtube/customisation2.png)

Search results can be customised to display additional fields and
ordered by various criteria.

This configuration was set up using the following commands
```
set order views
set columns user:14 date comments rating likes dislikes category:9 views
```

Type `help config` for help on configuration options

Upgrading
---------

Upgrade pip installation::

    pipx upgrade yewtube

Usage
-----

yewtube is run on the command line using the command:

   `yt`

Enter `h` from within the program for help.

How to Contribute
-----------------

Contributions are welcomed! However, please check out the [contribution page](https://github.com/iamtalhaasghar/yewtube/blob/develop/CONTRIBUTING.md) before making a contribution.

