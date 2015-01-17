#!/bin/sh

MPRIS_PATH=~/Python/mps-youtube/mps_youtube/mpris.py
MPSYT_PATH=~/Python/mps-youtube/mpsyt

python3 $MPRIS_PATH &
xterm -xrm 'xterm*allowSendEvents: true' -class mpsyt -e $MPSYT_PATH
pkill -f 'python3 .*mpris.py'