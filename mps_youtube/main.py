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

import locale
import logging
import os
import sys
import traceback as traceback_py
import click
from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.history import FileHistory

from . import g, c, commands, screen, history, init, util
from . import __version__, playlists, content
from . import config

has_readline = (
    True  # We use prompt_toolkit now, which provides equivalent features
)

mswin = os.name == "nt"

try:
    locale.setlocale(locale.LC_ALL, "")  # for date formatting
except Exception as err:
    logging.debug(f"locale not set: {err}")


def handle_command_exception(e):
    """Centralized error reporting for command execution."""
    if g.debug_mode:
        g.content = "".join(traceback_py.format_exception(*sys.exc_info()))

    if isinstance(e, IndexError):
        g.message = util.F("invalid range")
    elif isinstance(e, (ValueError, IOError)):
        g.message = util.F("cant get track") % str(e)
    else:
        template = util.F("no data")
        g.message = template % str(e) if "%s" in template else f"{template}: {e}"
        if not g.debug_mode:
            logging.debug(traceback_py.format_exc())

    g.content = g.content or content.generate_songlist_display()


def matchfunction(func, regex, userinput):
    """Match userinput against regex. Call func, return True if matches."""
    match = regex.match(userinput)
    if match and match.group(0) == userinput:
        matches = match.groups()
        util.dbg("input: %s", userinput)
        util.dbg("function call: %s", func.__name__)

        try:
            func(*matches)
        except Exception as e:
            handle_command_exception(e)

        return True


def prompt_for_exit(history=None, completer=None):
    """Ask for exit confirmation."""
    g.message = c.r + "Press ctrl-c again to exit" + c.w
    g.content = content.generate_songlist_display()
    screen.update()

    try:
        userinput = pt_prompt(
            c.r + " > " + c.w, history=history, completer=completer
        ).strip()

    except (KeyboardInterrupt, EOFError):
        commands.misc.quits(showlogo=False)

    return userinput


@click.command(
    context_settings=dict(
        help_option_names=["-h", "--help"], ignore_unknown_options=True
    )
)
@click.version_option(version=__version__)
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option(
    "--logging", "-l", "enable_logging", is_flag=True, help="Enable logging"
)
@click.option("--no-autosize", is_flag=True, help="Disable terminal autosizing")
@click.option("--no-preload", is_flag=True, help="Disable preloading of tracks")
@click.option("--no-textart", is_flag=True, help="Disable ASCII art")
@click.argument("commands_args", nargs=-1, type=click.UNPROCESSED)
def main(
    debug, enable_logging, no_autosize, no_preload, no_textart, commands_args
):
    """yewtube - Terminal based YouTube player and downloader."""

    # Setup global flags based on click options
    if debug or os.environ.get("mpsytdebug") == "1":
        g.debug_mode = True
        g.no_clear_screen = True

    if no_autosize:
        g.detectable_size = False

    if no_preload:
        g.preload_disabled = True

    if no_textart:
        g.no_textart = True

    g.argument_commands = list(commands_args)
    g.command_line = (
        "playurl" in g.argument_commands or "dlurl" in g.argument_commands
    )
    if g.command_line:
        g.no_clear_screen = True

    # Initialize
    try:
        init.init()
    except Exception as e:
        click.echo(f"Initialization failed: {e}", err=True)
        if g.debug_mode:
            traceback_py.print_exc()
        return sys.exit(1)

    if config.SET_TITLE.get:
        util.set_window_title("yewtube")

    if not g.command_line:
        g.content = content.logo(col=c.g, version=__version__) + "\n\n"
        g.message = "Enter /search-term to search or [h]elp"
        screen.update()

    # open playlists from file
    playlists.load()

    # open history from file
    history.load()

    # setup scrobbling
    commands.lastfm.init_network(verbose=False)
    prev_model = []
    scrobble_funcs = [commands.album_search.search_album]

    arg_inp = [
        cmd.replace(r",,", "[mpsyt-comma]") for cmd in g.argument_commands
    ]
    # Emulate the existing comma-split behavior for compatibility if args are concatenated
    if len(arg_inp) == 1 and "," in arg_inp[0]:
        arg_inp = arg_inp[0].split(",")

    prompt_str = "> "

    # Initialize prompt_toolkit history
    pt_history = FileHistory(g.READLINE_FILE) if g.READLINE_FILE else None

    while True:
        next_inp = ""

        if len(arg_inp):
            next_inp = arg_inp.pop(0).strip()
            next_inp = next_inp.replace("[mpsyt-comma]", ",")

        try:
            if next_inp:
                userinput = next_inp
            else:
                userinput = pt_prompt(
                    prompt_str,
                    completer=util.completer,
                    history=pt_history,
                    complete_while_typing=False,
                ).strip()

        except (KeyboardInterrupt, EOFError):
            userinput = prompt_for_exit(
                history=pt_history, completer=util.completer
            )

        try:
            matched = False
            for i in g.commands:
                if matchfunction(i.function, i.regex, userinput):
                    if (
                        prev_model != g.model
                        and i.function not in scrobble_funcs
                    ):
                        g.scrobble = False
                    prev_model = g.model
                    matched = True
                    break

            if not matched:
                g.content = g.content or content.generate_songlist_display()

                if g.command_line:
                    g.content = ""

                if userinput and not g.command_line:
                    g.message = c.b + "Bad syntax. Enter h for help" + c.w

                elif userinput and g.command_line:
                    sys.exit("Bad syntax")
        except Exception as e:
            if g.debug_mode:
                traceback_py.print_exc()
            g.message = f"{c.r}Error: {e}{c.w}"

        screen.update()
