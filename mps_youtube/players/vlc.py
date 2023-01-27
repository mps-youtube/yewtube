import os
import subprocess

from .. import config, g, util
from ..player import CmdPlayer


class vlc(CmdPlayer):
    def __init__(self, player):
        self.player = player

    def _generate_real_playerargs(self):
        args = config.PLAYERARGS.get.strip().split()

        pd = g.playerargs_defaults['vlc']
        args.extend((pd["title"], '"{0}"'.format(self.song.title)))

        if config.VLC_DUMMY_INTERFACE.get:
            print('[VLC DUMMY INTERFACE] Playing "{0}" ...'.format(self.song.title))
            args.extend(('-I', 'dummy')) # vlc without gui
        if not config.SHOW_VIDEO.get:
            args.extend(("--no-video",))

        util.list_update("--play-and-exit", args)

        return [self.player] + args + [self.stream['url']]

    def clean_up(self):
        self._kill_instance()

    def launch_player(self, cmd):
        with open(os.devnull, "w") as devnull:
            self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)
        self.p.wait()
        self.next()

    def _help(self, short=True):
        pass

    def _kill_instance(self):
        import os
        from sys import platform
        if platform == "linux" or platform == "linux2":
            os.system('pkill -f vlc')
        elif platform == "darwin":
            os.system('killall vlc')
        elif platform == "win32":
            os.system('taskkill /im vlc.exe /f') # https://stackoverflow.com/questions/49988/really-killing-a-process-in-windows
