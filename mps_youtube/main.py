"""
mps-youtube.

https://github.com/np1/mps-youtube

Copyright (C) 2014, 2015 np1 and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import traceback
import locale
import sys
import os

import pafy

from . import g, c, commands, screen, history, util
from . import __version__, playlists, content

try:
    import readline
    readline.set_history_length(2000)
    has_readline = True

except ImportError:
    has_readline = False


mswin = os.name == "nt"

locale.setlocale(locale.LC_ALL, "")  # for date formatting


def matchfunction(func, regex, userinput):
    """ Match userinput against regex.

    Call func, return True if matches.

    """
    # Not supported in python 3.3 or lower
    # match = regex.fullmatch(userinput)
    # if match:
    match = regex.match(userinput)
    if match and match.group(0) == userinput:
        matches = match.groups()
        util.dbg("input: %s", userinput)
        util.dbg("function call: %s", func.__name__)
        util.dbg("regx matches: %s", matches)

        try:
            func(*matches)

        except IndexError:
            if g.debug_mode:
                g.content = ''.join(traceback.format_exception(
                    *sys.exc_info()))
            g.message = util.F('invalid range')
            g.content = g.content or content.generate_songlist_display()

        except (ValueError, IOError) as e:
            if g.debug_mode:
                g.content = ''.join(traceback.format_exception(
                    *sys.exc_info()))
            g.message = util.F('cant get track') % str(e)
            g.content = g.content or\
                content.generate_songlist_display(zeromsg=g.message)

        except pafy.GdataError as e:
            if g.debug_mode:
                g.content = ''.join(traceback.format_exception(
                    *sys.exc_info()))
            g.message = util.F('no data') % e
            g.content = g.content

        return True


def prompt_for_exit():
    """ Ask for exit confirmation. """
    g.message = c.r + "Press ctrl-c again to exit" + c.w
    g.content = content.generate_songlist_display()
    screen.update()

    try:
        userinput = input(c.r + " > " + c.w)

    except (KeyboardInterrupt, EOFError):
        commands.misc.quits(showlogo=False)

    return userinput


def main():
    """ Main control loop. """
    util.set_window_title("mpsyt")

    if not g.command_line:
        g.content = content.logo(col=c.g, version=__version__) + "\n\n"
        g.message = "Enter /search-term to search or [h]elp"
        screen.update()

    # open playlists from file
    playlists.load()

    #open history from file
    history.load()

    arg_inp = ' '.join(g.argument_commands)

    prompt = "> "
    arg_inp = arg_inp.replace(r",,", "[mpsyt-comma]")
    arg_inp = arg_inp.split(",")

    while True:
        next_inp = ""

        if len(arg_inp):
            next_inp = arg_inp.pop(0).strip()
            next_inp = next_inp.replace("[mpsyt-comma]", ",")

        try:
            userinput = next_inp or input(prompt).strip()

        except (KeyboardInterrupt, EOFError):
            userinput = prompt_for_exit()

        for i in g.commands:
            if matchfunction(i.function, i.regex, userinput):
                break

        else:
            g.content = g.content or content.generate_songlist_display()

            if g.command_line:
                g.content = ""

            if userinput and not g.command_line:
                g.message = c.b + "Bad syntax. Enter h for help" + c.w

            elif userinput and g.command_line:
                sys.exit("Bad syntax")

        screen.update()
