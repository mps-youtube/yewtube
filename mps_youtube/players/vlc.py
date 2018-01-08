import os
import subprocess

from .. import config, util

from ..player import Player


class vlc(Player):
    def _generate_real_playerargs(self, song, override, stream, isvideo, softrepeat):
        args = config.PLAYERARGS.get.strip().split()

        util.list_update("--play-and-exit", args)

        return [config.PLAYER.get] + args + [stream['url']]

    def clean_up(self):
        pass

    def launch_player(self, cmd, song, songdata):
        with open(os.devnull, "w") as devnull:
            self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)
        returncode = self.p.wait()
        self.next()

    def _help(self, short=True):
        pass
