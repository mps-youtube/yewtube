pms
===

Search and stream music

usage: pms.py [-h] [-c N] query [query ...]

PMS Music Seeker

positional arguments:
  query            song and/or artist

optional arguments:
  -h, --help       show this help message and exit
  -c N, --count N  number of results


Usage Example:

# Play song immediately:

>./pms.py rolling stones paint it black
Searching for 'rolling stones paint it black'
+
  -----------------------------------------
  artist : The Rolling Stones 
  title  : Paint It Black 
  album  : Paint It Black 
  tags   : 60s, the rolling stones, british 
  size   : 5.34 MB
  -----------------------------------------

Playing - press [q] to quit..
>

# Get more results to choose from (-c argument)

>./pms.py -c7 michael jackson
Searching for 'michael jackson'
++-+++++

ITEM   SIZE    ARTIST                TRACK                  ALBUM                  
----   ----    ------                -----                  -----                  
1      8.2 Mb  Norwegian Recycling   Miracles [Bruno Mars   Norwegian Recycling    
2      7.6 Mb  Michael Jackson       Smooth Criminal (Radi  Bad                    
3      6.6 Mb  Michael Jackson       Come Together          History                
4      4.7 Mb  Michael Jackson       Thriller               Top 1000 Pop Hits of th
5      9.8 Mb  Michael Jackson       Smooth Criminal        Not Guilty (Special Fan
6      5.4 Mb  Michael Jackson       PYT (Pretty Young Thi  Thriller (25th Annivers
7      3.7 Mb  Michael Jackson       Bad                    unknown album          


[1-7] or [q]uit  : 5

  -----------------------------------------
  artist : Michael Jackson 
  title  : Smooth Criminal 
  album  : Not Guilty (Special Fan Edition) 
  tags   : king of pop, dance, soul 
  size   : 9.82 MB
  -----------------------------------------

Playing - press [q] to quit..

