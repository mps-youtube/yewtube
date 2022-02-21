#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mps_youtube import mpris


def test_mprsi2controller_init():
    assert mpris.Mpris2Controller()
