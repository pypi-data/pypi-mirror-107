#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Tests that objects are synced
"""


def test_objects_match():
    import sys
    sys.path.append('./installer')
    from mitoinstaller.user_install import USER_JSON_DEFAULT as INSTALLER_USER_JSON_DEFAULT
    from mitosheet.user.user import USER_JSON_DEFAULT

    for key, value in INSTALLER_USER_JSON_DEFAULT.items():
        if key == 'user_salt':
            continue
        assert USER_JSON_DEFAULT[key] == value
