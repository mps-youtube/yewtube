#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from mps_youtube.players import mplayer


@pytest.mark.parametrize(
    "exename, exp_err",
    [
        ("", (OSError, PermissionError)),
        ("mplayersomething", FileNotFoundError),
    ],
)
def test_get_mplayer_version_no_mplayer(exename, exp_err):
    with pytest.raises(exp_err):
        mplayer._get_mplayer_version(exename)


def test_get_mplayer_version_invalid_input():
    with mock.patch("mps_youtube.players.mplayer.subprocess"), pytest.raises(TypeError):
        mplayer._get_mplayer_version(mock.MagicMock())


@pytest.mark.parametrize(
    "output, exp_res",
    [
        (
            "MPlayer Redxii-SVN-r38151-6.2.0 (x86_64) (C) 2000-2019 MPlayer Team...",
            38151,
        ),
        ("MPlayer SVN-r38151-6.2.0 (x86_64) (C) 2000-2019 MPlayer Team...", 38151),
        ("MPlayer 1.4 (Debian), built with gcc-10 (C) 2000-2019 MPlayer Team", (1, 4)),
    ],
)
def test_get_mplayer_version(output, exp_res):
    with mock.patch("mps_youtube.players.mplayer.subprocess") as m_subprocess:
        m_subprocess.check_output.return_value.decode.return_value = output
        assert mplayer._get_mplayer_version(mock.MagicMock()) == exp_res
