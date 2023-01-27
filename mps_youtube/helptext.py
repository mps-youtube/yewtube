"""
    Holds all help text
"""
import pathlib
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from . import c, g
from .util import F, get_near_name


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
        {2}x <number>{1} - copy item <number> url to clipboard. (See the note below)
        Note: This feature requires `pyperclip` which is installed automatically when you install yewtube but
        Linux users further need to install `xsel` or `xclip` manually using apt, dnf, pacman, zypper or whatever package manager you use.
        Visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error for more info.

        {2}q{1}, {2}quit{1} - exit yewtube
    """.format(c.ul, c.w, c.y)),
        ("search", "Searching and Retrieving", """
    {0}Searching and Retrieving{1}

    {2}set search_music false{1} - search all YouTube categories.
    {2}set search_music true{1}  - search only YouTube music category.

    {2}/<query>{1} or {2}.<query>{1} to search for videos. e.g., {2}/daft punk{1}
    Search Arguments:
    {2}-d, --duration{1}    Can be any/short/medium/long
    {2}-a, --after{1}       Date in {2}YYYY-MM-DD{1} or {2}YYYY-MM-DD{1}T{2}HH:MM{1} format
    {2}-l, --live{1}        Limit search to livestreams
    {2}-c, --category{1}    Search within a category, (number or string)
                      Available categories:
                      {2}{3}{1}

    {2}//<query>{1} or {2}..<query>{1} - search for YouTube playlists. e.g., \
    {2}//80's music{1}
    {2}n{1} and {2}p{1} - continue search to next/previous pages.
    {2}p <number>{1} - switch to page <number>.

    {2}album <album title>{1} - Search for matching tracks using album title
    {2}channels <Channel name>{1} - Search for channels by channelname
    {2}live <category>{1} - Search for livestreams from a range of categories.
    Categories: {2}{3}{1}

    {2}mkp <fullfilepath>{1} - Creates a playlist automatically with video titles from fullfilepath
    <fullfilepath>: Full path of text file with one title per line

    {2}mkp -d <search result number>{1} - Create a playlist based on tracks
    listed in that videos description. (Alternatively one can use {2}--description{1})

    {2}user <username>{1} - list YouTube uploads by <username>.
    {2}user <username>/<query>{1} - as above, but matches <query>.
    {2}userpl <username>{1} - list YouTube playlists created by <username>.
    {2}pl <url or id>{1} - Open YouTube playlist by url or id.
    {2}url <url or id>{1} - Retrieve specific YouTube video by url or id.
    {2}url <url> <url> ... <url>{1} - Retrieve specific YouTube videos by url or id.
    {2}url_file <file_absolute_path>{1} - Retrieve YouTube videos by url or id from a .txt file.
    File format : .txt, with one url or id by line.

    {2}r <number>{1} - show videos related to video <number>.
    {2}u <number>{1} - show videos uploaded by uploader of video <number>.
    {2}c <number>{1} - view comments for video <number>
    """.format(c.ul, c.w, c.y, ", ".join(g.categories.keys()))),

        ("edit", "Editing / Manipulating Results", """
    {0}Editing and Manipulating Results{1}

    {2}rm <number(s)>{1} - remove items from displayed results.
    {2}sw <number>,<number>{1} - swap two items.
    {2}mv <number>,<number>{1} - move item <number> to position <number>.
    {2}save <name>{1} - save displayed items as a local playlist.
    {2}mix <number>{1} - show YouTube mix playlist from item in results.

    {2}shuffle{1} - Shuffle the displayed results.
    {2}shuffle all{1} - Shuffle entire loaded playlist.
    {2}reverse{1} or {2}reverse <number>-<number>{1} - Reverse the displayed items or item range.
    {2}reverse all{1} - Reverse order of entire loaded playlist.
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
    {2}dlurl <url or id>{1} - download a YouTube video by url or video id.
    {2}daurl <url or id>{1} - download best available audio of YouTube video by url or video id.
    {2}playurl <url or id>{1} - play a YouTube video by url or id.
    {2}browserplay <number>{1} - open a specified previous search in browser.

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
    %i - youtube video id

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

        ("history", "Accessing Local History", """
    {0}Accessing Local History{1}

    Access songs that have been played within yewtube

        {2}history{1} - displays a list of songs contained in history
        {2}history clear{1} - clears the song history
        {2}history recent{1} - displays a list of recent played songs
        {2}set history on|off{1} - toggles history recording
    """.format(c.ul, c.w, c.y)),

        ("invoke", "Invocation Parameters", """
    {0}Invocation{1}

    All yewtube commands can be entered from the command line.  For example;

      {2}yt dlurl <url or id>{1} to download a YouTube video by url or id
      {2}yt playurl <url or id>{1} to play a YouTube video by url or id
      {2}yt /mozart{1} to search
      {2}yt //best songs of 2010{1} for a playlist search
      {2}yt play <playlist name or ID>{1} to play a saved playlist
      {2}yt ls{1} to list saved playlists

    For further automation, a series of commands can be entered separated by
    commas (,).  E.g.,

      {2}yt open 1, 2-4{1} - play items 2-4 of first saved playlist
      {2}yt //the doors, 1, all -a{1} - open YouTube playlist and play audio

    If you need to enter an actual comma on the command line, use {2},,{1} instead.
    """.format(c.ul, c.w, c.y)),

        ("config", "Configuration Options", """
    {0}Configuration{1}

    {2}set{1} - view current configuration
    {2}set <item> default{1} - set an item to its default value
    {2}set all default{1} - restore default settings
    {2}set checkupdate true|false{1} - check for updates on exit
    {2}set columns <columns>{1} - select extra displayed fields in search results:
         (valid: views comments rating date time user likes dislikes category ytid)
    {2}set ddir <download direcory>{1} - set where downloads are saved
    {2}set download_command <command>{1} - type {2}help dl-command{1} for info
    {2}set encoder <number>{1} - set encoding preset for downloaded files
    {2}set fullscreen true|false{1} - output video content in full-screen mode
    {2}set always_repeat true|false{1} - always in repeat mode without repeat <number>
    {2}set max_res <number>{1} - play / download maximum video resolution height{3}
    {2}set notifier <notifier app>{1} - call <notifier app> with each new song title
    {2}set order <relevance|date|views|rating>{1} search result ordering
    {2}set user_order <<nothing>|relevance|date|views|rating>{1} user upload list
        result ordering, leave blank for the same as order setting
    {2}set overwrite true|false{1} - overwrite existing files (skip if false)
    {2}set player <player app>{1} - use <player app> for playback
    {2}set playerargs <args>{1} - use specified arguments with player
    {2}set lookup_metadata true|false{1} - lookup metadata using Last.fm
    {2}set lastfm_username <username>{1} - scrobble to this Last.fm userprofile
    {2}set lastfm_password <password>{1} - Last.fm password (saved in hash form)
    {2}set lastfm_api <key>{1} - API key needed for Last.fm mps-yt authorization
    {2}set lastfm_secret <key>{1} - secret for the Last.fm API key
    {2}set search_music true|false{1} - search only music (all categories if false)
    {2}set show_mplayer_keys true|false{1} - show keyboard help for mplayer and mpv
    {2}set show_status true|false{1} - show status messages and progress
    {2}set show_video true|false{1} - show video output (audio only if false)
    {2}set window_pos <top|bottom>-<left|right>{1} - set player window position
    {2}set window_size <number>x<number>{1} - set player window width & height
    {2}set audio_format <auto|m4a|webm>{1} - set default music audio format
    {2}set video_format <auto|mp4|webm|3gp>{1} - set default music video format
    {2}set set_title true|false{1} - change window title
    {2}set show_qrcode true|false{1} - show qrcode of the URL in the video information panel
    {2}set history true|false{1} - record play history
    {2}set input_history true|false{1} - record command input history
    {2}set vlc_dummy_interface true|false{1} - whether to hide VLC GUI or not (hides when true)

    Additionally, {2}set -t{1} may be used to temporarily change a setting without
    saving it to disk
    """.format(c.ul, c.w, c.y, '\n{0}set max_results <number>{1} - show <number> re'
               'sults when searching (max 50)'.format(c.y, c.w) if not
               g.detectable_size else '')),

        ("lastfm", "Last.fm configuration", """
    {0}Configure Last.fm{1}

    pylast needs to be installed for Last.fm support. See https://github.com/pylast/pylast.

    Use {2}set{1} to set your Last.fm login credenditals, e.g. {2}set lastfm_username jane_doe{1}.
    Similarly, you also have to provide an API key and it's corresponding secret.
    An API key can be retrieved from https://www.last.fm/api/account/create.

    Your Last.fm configuration is saved and automatically reloaded when mps-youtube starts.

    After having set the required information, a connection can also be established
    with {2}lastfm_connect{1}. Additionally, {2}lastfm_connect{1} provides verbose error messages.

    For now, Last.fm support only works with the {2}album{1} command.
    """.format(c.ul, c.w, c.y)),

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

    Use {2}clearcache{1} command to clear the cache.
    """.format(
                c.ul, c.w, c.y
            ),
        ),
        (
            "new",
            "Check if new version is available",
            """{0}What's New{1}\n{3}""".format(c.ul, c.w, c.y, "get_changelog()"),
        ),
        (
            "changelog",
            "Check program changelog",
            """{0}Changelog{1}\n{3}""".format(c.ul, c.w, c.y, "get_changelog_local()"),
        ),
        (
            "tor",
            "Check Tor Status. NOTE: Use this feature at your own risk. In case of any kind of damage we will not be responsible.",
            """{0}Tor Status{1}\n{3}""".format(c.ul, c.w, c.y, "check_tor()"),
        ),
    ]


def get_help(choice):
    """ Return help message. """
    helps = {"download": ("playback dl listen watch show repeat playing"
                          "show_video playurl browserplay dlurl d da dv all *"
                          " play browsersearch".split()),

             "dl-command": ("dlcmd dl-cmd download-cmd dl_cmd download_cmd "
                            "download-command download_command".split()),

             "encode": ("encoding transcoding transcode wma mp3 format "
                        "encode encoder".split()),

             "invoke": "command commands yt invocation".split(),

             "search": ("user userpl pl pls r n p url album "
                        "editing result results related remove swop mkp --description".split()),

             "edit": ("editing manupulate manipulating rm mv sw edit move "
                      "swap shuffle".split()),

             "tips": ("undump dump -f -w -a adv advanced".split(" ")),

             "basic": ("basic comment basics c copy clipboard comments u "
                       "i".split()),

             "config": ("set checkupdate colours colors ddir directory player "
                        "arguments args playerargs music search_music keys "
                        "status show_status show_video video configuration "
                        "fullscreen full screen folder player mpv mplayer"
                        " settings default reset configure audio results "
                        "max_results size lines rows height window "
                        "position window_pos quality resolution max_res "
                        "columns width console overwrite".split()),

             "playlists": ("save rename delete move rm ls mv sw add vp open"
                           " view".split())}

    for topic, aliases in helps.items():

        if choice in aliases:
            choice = topic
            break

    choice = "menu" if not choice else choice
    out, all_help = "", helptext()
    help_names = [x[0] for x in all_help]
    choice = get_near_name(choice, help_names)

    def indent(x):
        """ Indent. """
        return "\n  ".join(x.split("\n"))

    if choice == "menu" or choice not in help_names:
        out += "  %sHelp Topics%s" % (c.ul, c.w)
        out += F('help topic', 2, 1)

        for x in all_help:
            out += ("\n%s     %-10s%s : %s" % (c.y, x[0], c.w, x[1]))

        out += "\n"
        return out

    else:
        if choice == 'tor':
            output_text = check_tor()
        elif choice == 'new':
            output_text = get_changelog()
        elif choice == "changelog":
            output_text = get_changelog_local()
        else:
            choice = help_names.index(choice)
            output_text = all_help[choice][2]

        return indent(output_text)

def get_changelog():
    try:
        url = "https://raw.githubusercontent.com/iamtalhaasghar/yewtube/master/CHANGELOG.md"
        v = urlopen(url, timeout=1).read().decode()
        v = v.split('## v')[1]
        return v
    except (URLError, HTTPError, socket.timeout):
        return "read changelog timed out"


def get_changelog_local():
    cl_path = pathlib.Path(__file__).parent.parent / "CHANGELOG.md"
    if cl_path.is_file():
        return "\n".join(reversed(cl_path.read_text().splitlines()))
    else:
        return "can't find changelog file"


def check_tor():
    try:
        url = "https://check.torproject.org/?lang=en"
        v = urlopen(url, timeout=1).read().decode()
        ip = re.findall('<strong>(.*)</strong>', v)
        status = re.findall('Congratulations.(.*)', v)
        if len(status) == 0:
            status = re.findall('Sorry.(.*)', v)
        return str({'ip' : ip, 'status': status[0]})
    except (URLError, HTTPError, socket.timeout):
        return "read check tor status timed out"
