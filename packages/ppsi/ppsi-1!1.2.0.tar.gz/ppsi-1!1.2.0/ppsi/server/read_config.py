#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Load yaml configuration file(s), temp storage folder

Load {action: '--flag', ...} for all available menus
Determine a root directory for temporary storage and log files
'''

import os
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

from .sway_api import sway_nag


def get_defaults() -> Tuple[Path, Path]:
    '''
    Returns:
        swayroot: Confirmed existing Path for sway files
        config: dictionary of default config fetched from default locations

    get default values
    '''
    # Shipped defaults
    swayroot = Path(__file__).parent.joinpath('config')
    config = swayroot.joinpath('ppsi.yml')

    def_loc: List[Tuple[Optional[str], Tuple[str, ...]]] = [
        (os.environ.get('XDG_CONFIG_HOME', None), ('sway', )),  # Good practice
        (os.environ.get('HOME', None), ('.config', 'sway')),  # The same thing
    ]
    for location in def_loc:
        if location[0] is not None:
            test_root = Path(location[0]).joinpath(*location[1])
            if test_root.is_dir():
                swayroot = test_root
                break

    # default config
    for location in def_loc:
        if location[0] is not None:
            test_conf = Path(location[0]).joinpath(*location[1], 'ppsi.yml')
            if test_conf.is_file():
                config = test_conf
                break
    return swayroot, config


def read_config(custom_conf: os.PathLike = None,
                swayroot: os.PathLike = None) -> Tuple[Path, dict]:
    '''
    Read ppsi configuration from supplied yml file or default
    Define swayroot to store log files.

    Args:
        custom_conf: custom path of config file ppsi.yml
        swayroot: custom path of root directory to store sway data

    Returns:
        swayroot, config referenced by ``menu``
    '''
    # default locations
    defroot, defconfig = get_defaults()
    if swayroot is None:
        swayroot = defroot
    swayroot = Path(swayroot)
    if custom_conf is None:
        root_path = Path(swayroot).joinpath("ppsi.yml")
        if root_path.is_file():
            custom_conf = root_path
    config = {}
    with open(defconfig, "r") as config_h:
        try:
            config = yaml.safe_load(config_h)
        except (FileNotFoundError, yaml.composer.ComposerError) as err:
            sway_nag(msg=str(err), error=True)
    if custom_conf is not None:
        with open(custom_conf, "r") as config_h:
            try:
                config = yaml.safe_load(config_h)
            except (FileNotFoundError, yaml.composer.ComposerError) as err:
                sway_nag(msg=str(err), error=True)
    return swayroot.absolute(), config
