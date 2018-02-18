import os
import subprocess

from .. import config, util

from ..player import CmdPlayer


class vlc(CmdPlayer):
    def __init__(self, player):
        self.player = player

    def _generate_real_playerargs(self):
        args = config.PLAYERARGS.get.strip().split()

        util.list_update("--play-and-exit", args)

        return [self.player] + args + [self.stream['url']]

    def clean_up(self):
        pass

    def launch_player(self, cmd):
        with open(os.devnull, "w") as devnull:
            self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)
        self.p.wait()
        self.next()

    def _help(self, short=True):
        pass
