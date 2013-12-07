pms
===

 - Search and stream music
 - Download music
 - Works with Python 2.7 and 3.x
 - Works with Windows, Linux and Mac OSX 10.9
 - No Python dependencies
 - Requires mplayer

# Installation:

Using pip:
    
    sudo pip install Poor-Mans-Spotify
    
Using git:

    git clone https://github.com/np1/pms.git

Manually:

Download [zip](https://github.com/np1/pms/archive/master.zip)/[tar.gz](https://github.com/np1/pms/archive/master.tar.gz) file and extract

# Special instruction for Mac OSX.
    
    Download mplayer: https://www.macupdate.com/app/mac/18580/mplayer
    Make a link for mplayer: ln -s /Applications/MPlayer OSX.app/Contents/Resources/External_Binaries/mplayer.app/Contents/MacOS/mplayer /usr/local/bin/mplayer
    Install X11: http://xquartz.macosforge.org/landing/
    
    NOTE - for MplayerX: ln -s /Applications/MPlayerX.app/Contents/Resources/binaries/x86_64/mplayer /usr/local/bin/mplayer
# Usage

    usage: pms query [query ...]

    or simply:

    pms
# Advance usage
    \list [url]
    \top \top3m \top6m \topyear \topall

# Screenshot
![pms running in terminal](http://i.imgur.com/Oqyz5vk.png "pms running in terminal")

# Usage Example:

    $ > ls
    LICENSE  pms  README.md
    $ > ./pms
    Enter artist/song to search : gotye somebody i used to know

    Search for 'gotye somebody i used to know'

    Item   Size    Artist                Track                  Length   Bitrate 
    ----   ----    ------                -----                  ------   ------- 
    1      3.7 Mb  Gotye feat. Kimbra    Somebody That I Used   04:04    128     
    2      9.3 Mb  Gotye                 Somebody That I Used   04:04    320     
    3      5.5 Mb  Gotye                 Somebody That I Used   04:03    192     
    4      9.1 Mb  Gotye feat. Kimbra    Somebody That I Used   04:00    320     
    5      4.0 Mb  Walk off the Earth    Somebody That I Used   04:24    128     
    6      9.1 Mb  Gotye feat. Kimbra    Somebody That I Used   04:00    320     
    7      6.3 Mb  Gotye feat. Kimbra    Somebody That I Used   04:05    VBR     
    8      6.8 Mb  Gotye                 Somebody That I Used   04:04    VBR     
    9      9.3 Mb  Gotye feat. Kimbra    Somebody That I Used   04:03    320     
    10     5.3 Mb  Gotye feat. Kimbra    Somebody that I used   04:05    VBR     
    11     9.5 Mb  Gotye ft. Kimbra      Somebody That I Used   04:05    VBR     
    12     7.3 Mb  DFM RADIO             Gotye feat. Kimbra- S  03:13    320     
    13     8.0 Mb  Somebody That I Used  Walk off the Earth (G  04:24    VBR     
    14     7.4 Mb  Gotye                 Somebody That I Used   04:05    256     
    15     5.4 Mb  Gotye feat. kimbra    Somebody that I used   05:55    128     
    16     5.9 Mb  Gotye Feat. Kimbra &  Somebody That I Used   03:15    256     
    17     3.1 Mb  Pentatonix            Somebody That I Used   03:25    VBR     
    18     9.2 Mb  Gotye feat. Kimbra    Somebody That I Used   04:02    320     
    19     13. Mb  Gotye ft. Kimbra      Somebody That I Used   05:30    320     
    20     9.3 Mb  Gotye feat Kimbra     Somebody That I Used   04:04    320     

    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > 3

      -----------------------------------------------------
      Artist  : Gotye
      Title   : Somebody That I Used To Know (feat. Kimbra)
      Length  : 04:03
      Bitrate : 192 Kb/s
      Size    : 5.594 Mb
      -----------------------------------------------------

    Playing - [q] to quit..



--

    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > d3



    Downloading /f/h/Downloads/PMS/Gotye - Somebody That I Used To Know (.mp3 ..
      5,865,433 Bytes [100.00%] received. Rate: [ 734 kbps].  ETA: [0 secs]    
    Done


--



    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > avicii

    Search for 'avicii'

    Item   Size    Artist                Track                  Length   Bitrate 
    ----   ----    ------                -----                  ------   ------- 
    1      9.5 Mb  Avicii feat. Aloe Bl  Wake Me Up             04:09    320     
    2      18. Mb  Tim Berg              Bromance (The Love Yo  08:10    320     
    3      7.5 Mb  Avicii vs Nicky Rome  I Could Be The One     05:29    VBR     
    4      10. Mb  Avicii                Levels (Skrillex Remi  04:41    320     
    5      13. Mb  Avicii                Malo (Alex Gaudino &   06:00    320     
    6      12. Mb  Avicii                Levels                 05:33    VBR     
    7      5.8 Mb  Sebastien Drums & Av  My Feelings For You    06:24    128     
    8      16. Mb  Nadia Ali             Rapture (Avicii New G  07:08    320     
    9      7.7 Mb  Tim Berg              Seek Bromance (Avicii  03:21    320     
    10     13. Mb  Tim Berg              Bromance (Avicii's Ar  06:00    320     
    11     12. Mb  Avicii                Levels (Original Mix)  05:33    VBR     
    12     6.1 Mb  Tim Berg              Seek Bromance (Avicii  03:21    256     
    13     9.7 Mb  Avicii                Wake Me Up (Radio Edi  04:09    VBR     
    14     4.5 Mb  Avicii Ft Etta James  ID (Levels) (Original  03:17    192     
    15     7.9 Mb  Avicii vs. Nicky Rom  I Could Be The One (R  03:28    320     
    16     5.8 Mb  Avicii                Fade Into Darkness     03:14    VBR     
    17     9.1 Mb  Armin Van Buuren Fea  Drowing (Avicii Unnam  04:00    320     
    18     7.7 Mb  Avicii                Levels (Radio Edit)    03:21    VBR     
    19     7.9 Mb  Avicii & Nicky Romer  I Could Be The One (R  03:12    320     
    20     13. Mb  David Guetta          Sunshine (David Guett  06:00    VBR     

    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > 3

      --------------------------------
      Artist  : Avicii vs Nicky Romero
      Title   : I Could Be The One
      Length  : 05:29
      Bitrate : VBR
      Size    : 7.534 Mb
      --------------------------------

    Playing - [q] to quit..


    [1-20] to play or [d 1-20] to download or [q]uit or enter new search
     > 
