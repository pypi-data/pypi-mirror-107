#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for raytraverse.scene"""
import os
import shutil

import pytest
from raytraverse.example import main, out, scene_files, zone, epw, output


@pytest.fixture(scope="module")
def tmpdir(tmp_path_factory):
    data = str(tmp_path_factory.mktemp("data"))
    subf = 'tests/example/'
    shutil.copytree(subf, data + '/test')
    cpath = os.getcwd()
    path = data + '/test'
    # uncomment to use actual (to debug results)
    # path = cpath + '/' + subf
    os.chdir(path)
    yield path
    os.chdir(cpath)

def test_example(tmpdir):
    with cap
