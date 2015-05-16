# https://gist.github.com/jtriley/1108174

""" Terminal Size. """

import os
import sys
import shlex
import shutil
import struct
import platform
import subprocess


def get_terminal_size():
    """ getTerminalSize().

    - get width and height of console
    - works on linux,os x,windows,cygwin(windows)
    originally retrieved from:
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """

    if sys.version_info >= (3,3):
        return shutil.get_terminal_size()

    current_os = platform.system()
    tuple_xy = None

    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()

        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!

    else:
        tuple_xy = _get_terminal_size_linux()

    if tuple_xy is None:
        tuple_xy = (80, 25)      # default value

    return tuple_xy


def _get_terminal_size_windows():
    """ Get terminal size on MS Windows. """
    # pylint: disable=R0914
    # too many local variables
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey

    except:
        pass


def _get_terminal_size_tput():
    """ Get terminal size using tput. """
    # src: http://stackoverflow.com/questions/263890/
    # how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    """ Get terminal size Linux. """
    def ioctl_GWINSZ(fd):
        """ ioctl_GWINSZ. """
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr

        except:
            pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr or cr == (0, 0):

        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)

        except:
            pass

    if not cr or cr == (0, 0):

        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])

        except:
            return

    return int(cr[1]), int(cr[0])
