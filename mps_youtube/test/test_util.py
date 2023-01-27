#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import mps_youtube.util as util


@pytest.mark.parametrize(
    "num,t,exp_res",
    (
        (0, "", ""),
        (0, None, ""),
    ),
)
def test_uea_pad(num, t, exp_res):
    res = util.uea_pad(num, t)
    assert res == exp_res
