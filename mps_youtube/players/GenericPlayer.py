import os
import subprocess

from .. import config

from ..player import CmdPlayer

#
# This class can be used as a templete for new players
#
# NOTE:
# If you're defining a new player donot forget
# to name both the class and file the same as your player
#


class GenericPlayer(CmdPlayer):
    def __init__(self, player):
        self.player = player

    def _generate_real_playerargs(self):
        '''Generates player arguments to called using Popen

        '''
        args = config.PLAYERARGS.get.strip().split()

        ############################################
        # Define your arguments below this line

        ###########################################

        return [self.player] + args + [self.stream['url']]

    def clean_up(self):
        ''' Cleans up temp files after process exits.

        '''
        pass

    def launch_player(self, cmd):

        ##################################################
        # Change this however you want

        with open(os.devnull, "w") as devnull:
            self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)
        self.p.wait()

        ##################################################

        # Donot forget self.next()
        self.next()

    def _help(self, short=True):
        ''' Help keys shown when the song is played.

        See mpv.py for reference.

        '''
        pass
