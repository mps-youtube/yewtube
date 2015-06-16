from . import c, g


def helptext():
    """ Return a list of help categories, with their contents. """

    return [
        ("basic", "Basics", """

    {0}Basic Usage{1}

    Use {2}/{1} or {2}.{1} to prefix your search query.  e.g., {2}/pink floyd{1}

    Then, when results are shown:

        {2}<number(s)>{1} - play specified items, separated by commas.
                      e.g., {2}1-3,5{1} plays items 1, 2, 3 and 5.

        {2}i <number>{1} - view information on video <number>
        {2}c <number>{1} - view comments for video <number>
        {2}d <number>{1} - download video <number>
        {2}r <number>{1} - show videos related to video <number>
        {2}u <number>{1} - show videos uploaded by uploader of video <number>
        {2}x <number>{1} - copy item <number> url to clipboard (requires pyperclip)

        {2}q{1}, {2}quit{1} - exit mpsyt
    """.format(c.ul, c.w, c.y)),
        ("search", "Searching and Retrieving", """
    {0}Searching and Retrieving{1}

    {2}set search_music false{1} - search all YouTube categories.
    {2}set search_music true{1}  - search only YouTube music category.

    {2}/<query>{1} or {2}.<query>{1} to search for videos. e.g., {2}/daft punk{1}
    {2}//<query>{1} or {2}..<query>{1} - search for YouTube playlists. e.g., \
    {2}//80's music{1}
    {2}n{1} and {2}p{1} - continue search to next/previous pages.
    {2}p <number>{1} - switch to page <number>.

    {2}album <album title>{1} - Search for matching tracks using album title
    {2}user <username>{1} - list YouTube uploads by <username>.
    {2}user <username>/<query>{1} - as above, but matches <query>.
    {2}userpl <username>{1} - list YouTube playlists created by <username>.
    {2}pl <url or id>{1} - Open YouTube playlist by url or id.
    {2}url <url or id>{1} - Retrieve specific YouTube video by url or id.

    {2}r <number>{1} - show videos related to video <number>.
    {2}u <number>{1} - show videos uploaded by uploader of video <number>.
    {2}c <number>{1} - view comments for video <number>
    """.format(c.ul, c.w, c.y)),

        ("edit", "Editing / Manipulating Results", """
    {0}Editing and Manipulating Results{1}

    {2}rm <number(s)>{1} - remove items from displayed results.
    {2}sw <number>,<number>{1} - swap two items.
    {2}mv <number>,<number>{1} - move item <number> to position <number>.
    {2}save <name>{1} - save displayed items as a local playlist.
    {2}mix <number>{1} - show YouTube mix playlist from item in results.

    {2}shuffle{1} - Shuffle the displayed results.
    """.format(c.ul, c.w, c.y)),

        ("download", "Downloading and Playback", """
    {0}Downloading and Playback{1}

    {2}set show_video true{1} - play video instead of audio.

    {2}<number(s)>{1} - play specified items, separated by commas.
                  e.g., {2}1-3,5{1} plays items 1, 2, 3 and 5

    {2}d <number>{1} - view downloads available for an item.
    {2}da <number(s)>{1} - download best available audio file(s).
    {2}dv <number(s)>{1} - download best available video file(s).
    {2}dapl <url or id>{1} - download YouTube playlist (audio) by url or id.
    {2}dvpl <url or id>{1} - download YouTube playlist (video) by url or id.
    {2}daupl <username>{1} - download user's YouTube playlists (audio).
    {2}dvupl <username>{1} - download user's YouTube playlists (video).
    {2}dlurl <url or id>{1} download a YouTube video by url or video id.
    {2}playurl <url or id>{1} play a YouTube video by url or id.

    {2}all{1} or {2}*{1} - play all displayed items.
    {2}repeat <number(s)>{1} - play and repeat the specified items.
    {2}shuffle <number(s)>{1} - play specified items in random order.
    """.format(c.ul, c.w, c.y)),

        ("dl-command", "Downloading Using External Application", """
    {0}Download Using A Custom Application{1}

    Use {2}set download_command <command>{1} to specify a custom command to use for
    downloading.

    mps-youtube will make the following substitutions:

    %u - url of the remote file to download
    %d - download directory as set in DDIR in mps-youtube config
    %f - filename (determined by title and filetype)
    %F - full file path (%d/%f)

    for example, to download using aria2c (http://aria2.sourceforge.net), enter:

        {2}set download_command aria2c --dir=%d --out=%f %u{1}

    Note that using a custom download command does not support transcoding the
    downloaded file to another format using mps-youtube.
    """.format(c.ul, c.w, c.y)),


        ("encode", "Encoding to MP3 and other formats", """
    {0}Encoding to MP3 and other formats{1}

    Enter {2}encoders{1} to view available encoding presets
    Enter {2}set encoder <number>{1} to apply an encoding preset for downloads

    This feature requires that ffmpeg or avconv is installed on your system and is
    available in the system path.

    The encoding presets can be modified by editing the text config file which
    resides at:
       {3}
    """.format(c.ul, c.w, c.y, g.TCFILE)),

        ("playlists", "Using Local Playlists", """
    {0}Using Local Playlists{1}

    {2}add <number(s)>{1} - add items to the current playlist.
    {2}add <number(s)> <playlist>{1} - add items to the specified playlist.
         (<playlist> will be created if it doesn't already exist)

    {2}vp{1} - view current playlist.
    {2}ls{1} - list saved playlists.
    {2}mv <old name or ID> <new name>{1} - rename a playlist.
    {2}rmp <playlist_name or ID>{1} - delete a playlist from disk.

    {2}open <name or ID>{1} - open a saved playlist as the current playlist.
    {2}play <name or ID>{1} - play a saved playlist directly.
    {2}view <name or ID>{1} - view a playlist (current playlist left intact).
    {2}save{1} or {2}save <name>{1} - save the displayed items as a playlist.

    {2}rm <number(s)>{1} - remove items from displayed results.
    {2}sw <number>,<number>{1} - swap two items.
    {2}mv <number>,<number>{1} - move item <number> to position <number>.
    """.format(c.ul, c.w, c.y)),

        ("invoke", "Invocation Parameters", """
    {0}Invocation{1}

    All mpsyt commands can be entered from the command line.  For example;

      {2}mpsyt dlurl <url or id>{1} to download a YouTube video by url or id
      {2}mpsyt playurl <url or id>{1} to play a YouTube video by url or id
      {2}mpsyt /mozart{1} to search
      {2}mpsyt //best songs of 2010{1} for a playlist search
      {2}mpsyt play <playlist name or ID>{1} to play a saved playlist
      {2}mpsyt ls{1} to list saved playlists

    For further automation, a series of commands can be entered separated by
    commas (,).  E.g.,

      {2}mpsyt open 1, 2-4{1} - play items 2-4 of first saved playlist
      {2}mpsyt //the doors, 1, all -a{1} - open YouTube playlist and play audio

    If you need to enter an actual comma on the command line, use {2},,{1} instead.
    """.format(c.ul, c.w, c.y)),

        ("config", "Configuration Options", """
    {0}Configuration{1}

    {2}set{1} - view current configuration
    {2}set <item> default{1} - set an item to its default value
    {2}set all default{1} - restore default settings
    {2}set checkupdate true|false{1} - check for updates on exit
    {2}set colours true|false{1} - use colours in display output
    {2}set columns <columns>{1} - select extra displayed fields in search results:
         (valid: views comments rating date user likes dislikes category)
    {2}set ddir <download direcory>{1} - set where downloads are saved
    {2}set download_command <command>{1} - type {2}help dl-command{1} for info
    {2}set encoder <number>{1} - set encoding preset for downloaded files
    {2}set fullscreen true|false{1} - output video content in full-screen mode
    {2}set max_res <number>{1} - play / download maximum video resolution height{3}
    {2}set notifier <notifier app>{1} - call <notifier app> with each new song title
    {2}set order <relevance|date|views|rating>{1} search result ordering
    {2}set user_order <<nothing>|relevance|date|views|rating>{1} user upload list
        result ordering, leave blank for the same as order setting
    {2}set overwrite true|false{1} - overwrite existing files (skip if false)
    {2}set player <player app>{1} - use <player app> for playback
    {2}set playerargs <args>{1} - use specified arguments with player
    {2}set search_music true|false{1} - search only music (all categories if false)
    {2}set show_mplayer_keys true|false{1} - show keyboard help for mplayer and mpv
    {2}set show_status true|false{1} - show status messages and progress
    {2}set show_video true|false{1} - show video output (audio only if false)
    {2}set window_pos <top|bottom>-<left|right>{1} - set player window position
    {2}set window_size <number>x<number>{1} - set player window width & height
    {2}set api_key <key>{1} - use a different API key for accessing the YouTube Data API
    """.format(c.ul, c.w, c.y, '\n{0}set max_results <number>{1} - show <number> re'
               'sults when searching (max 50)'.format(c.y, c.w) if not
               g.detectable_size else '')),

        ("tips", "Advanced Tips", """
    {0}Advanced Tips{1}

    Use {2}-w{1}, {2}-f{1} or {2}-a{1} with your choice to override the configured\
     setting and
    play items in windowed, fullscreen or audio modes.  E.g., 1-4 -a

    When specifying columns with {2}set columns{1} command, append :N to set\
     width.
        E.g.: {2}set columns date views user:17 likes{1}

    When using {2}open{1}, {2}view{1} or {2}play{1} to access a local playlist, \
    you can enter
    the first few characters instead of the whole name.

    Use {2}5-{1} to select items 5 upward and {2}-5{1} to select up to item 5. \
    This can be
    included with other choices. e.g., 5,3,7-,-2
    You can use spaces instead of commas: 5 3 7- -2
    Reversed ranges also work. eg., 5-2

    {2}dump{1} - to show entire contents of an opened YouTube playlist.
           (useful for playing or saving entire playlists, use {2}undump{1} to \
    undo)

    {2}set player mpv{1} or {2}set player mplayer{1} - change player application

    Use {2}1{1} and {2}0{1} in place of true and false when using the {2}set{1} \
    command
    """.format(c.ul, c.w, c.y)),

        ("new", "New Features", """
    {0}New Features in v0.2.2{1}

     - Display playing resolution / bitrate in status line (Brebiche38)

     - Skip to previously played item (ids1024)

     - Enable custom keymap using mplayer/mpv input.conf file (ids1024)

     - Enable custom downloader application (ids1024 & np1){2}

    """.format(c.ul, c.w, c.y))]
