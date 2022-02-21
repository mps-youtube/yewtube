#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

import dbus
import pytest

from mps_youtube import mpris


def test_mprsi2controller_init():
    assert mpris.Mpris2Controller()


def test_mpris2mediaplayer_init():
    bus = MagicMock()
    obj = mpris.Mpris2MediaPlayer(bus)
    assert obj
    v_obj = vars(obj)
    v_obj.pop("_locations_lock")
    #  '_locations_lock': <unlocked _thread.lock object at 0x7f0af1d20240>,
    assert vars(obj) == {
        "_connection": bus,
        "_fallback": False,
        "_locations": [(bus, "/org/mpris/MediaPlayer2", False)],
        "_name": None,
        "_object_path": "/org/mpris/MediaPlayer2",
        "fifo": None,
        "mpv": False,
        "properties": {
            "org.mpris.MediaPlayer2": {
                "read_only": {
                    "CanQuit": False,
                    "CanRaise": False,
                    "CanSetFullscreen": False,
                    "DesktopEntry": "mps-youtube",
                    "HasTrackList": False,
                    "Identity": "mps-youtube",
                    "SupportedMimeTypes": dbus.Array([], signature=dbus.Signature("s")),
                    "SupportedUriSchemes": dbus.Array(
                        [], signature=dbus.Signature("s")
                    ),
                },
                "read_write": {"Fullscreen": False},
            },
            "org.mpris.MediaPlayer2.Player": {
                "read_only": {
                    "CanControl": True,
                    "CanGoNext": True,
                    "CanGoPrevious": True,
                    "CanPause": True,
                    "CanPlay": True,
                    "CanSeek": True,
                    "MaximumRate": 1.0,
                    "Metadata": {
                        "mpris:trackid": dbus.ObjectPath(
                            "/CurrentPlaylist/UnknownTrack", variant_level=1
                        )
                    },
                    "MinimumRate": 1.0,
                    "PlaybackStatus": "Stopped",
                    "Position": dbus.Int64(0),
                },
                "read_write": {"Rate": 1.0, "Volume": 1.0},
            },
        },
        "socket": None,
    }


@pytest.mark.parametrize("val", (None, 0, 3, 5))
def test_mpris2mediaplayer_set_property_time_pos(val):
    obj = mpris.Mpris2MediaPlayer(MagicMock())
    obj.Seeked = MagicMock()
    obj.setproperty("time-pos", val)
    exp_res = dbus.Int64(val * 10**6) if val else dbus.Int64(0)
    assert obj.properties[mpris.PLAYER_INTERFACE]["read_only"]["Position"] == exp_res
    seeked_call_args = None
    try:
        seeked_call_args = obj.Seeked.mock_calls[0].args
    except IndexError:
        pass
    if val and val >= 4:
        assert seeked_call_args == (exp_res,)
    else:
        assert seeked_call_args is None


@pytest.mark.parametrize(
    "val1, val2",
    (
        (0, 2),
        (2, 6),
        (2, 5),
        (2, 7),
    ),
)
def test_mpris2mediaplayer_set_property_time_pos_seeked(val1, val2):
    obj = mpris.Mpris2MediaPlayer(MagicMock())
    obj.Seeked = MagicMock()
    obj.setproperty("time-pos", val1)
    obj.setproperty("time-pos", val2)
    seeked_call_args = None
    try:
        seeked_call_args = obj.Seeked.mock_calls[0].args
    except IndexError:
        pass
    d2 = dbus.Int64(val2 * 10**6)
    if abs(d2 - dbus.Int64(val1 * 10**6)) >= 4 * 10**6:
        assert seeked_call_args == (d2,)
    else:
        assert seeked_call_args is None
