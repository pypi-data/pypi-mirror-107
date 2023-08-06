# *****************************************************************************
# PILS PLC client library
# Copyright (c) 2019-2021 by the authors, see LICENSE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

"""Basic test suite for the devices in the testplc."""

import time

import pytest

from zapf import ApiError
from zapf.device import typecode_description
from zapf.spec import ParamCMDs, PLCStatus


def test_readable_device(plc_readable_device):
    """test value/status"""
    # zapf-device, TYPCODE_MAP entry
    dev, _tcme = plc_readable_device

    status = dev.read_status()
    state = status.STATE

    assert state in [PLCStatus.IDLE, PLCStatus.DISABLED,
                     PLCStatus.WARN, PLCStatus.START,
                     PLCStatus.BUSY, PLCStatus.STOP, PLCStatus.ERROR]
    assert dev.name == typecode_description(dev.typecode)

    value = dev.read_value()
    limits = dev.get_limits()
    assert limits[0] <= value <= limits[1]

    if not dev.target_addr:
        with pytest.raises(ApiError):
            dev.read_target()
        with pytest.raises(ApiError):
            dev.change_target(0)


def test_target_device(plc_target_device):
    """test target, moving around"""
    # zapf-device, TYPCODE_MAP entry
    dev, _tcme = plc_target_device

    status = dev.read_status()

    target = dev.read_target()
    limits = dev.get_limits()
    assert limits[0] <= target <= limits[1]

    # check precondition before starting a movement
    assert status.STATE not in [PLCStatus.START, PLCStatus.BUSY,
                                PLCStatus.STOP]
    assert status.STATE in [PLCStatus.IDLE, PLCStatus.WARN]

    value = dev.read_value()
    target = value + 1
    dev.change_target(target)
    assert dev.read_target() == target

    timesout = time.time() + 1
    # now check for end of movement
    while True:
        status = dev.read_status()
        value = dev.read_value()
        target = dev.read_target()
        assert status.STATE in [PLCStatus.START, PLCStatus.BUSY,
                                PLCStatus.IDLE, PLCStatus.WARN]
        if value != target:
            assert status.STATE == PLCStatus.BUSY
        if status.STATE != PLCStatus.BUSY:
            assert value == target
            return
        assert time.time() < timesout


def test_vector_devices(plc_vector_device):
    """test vector value/status/target/moving around"""
    # zapf-device, TYPCODE_MAP entry
    dev, tcme = plc_vector_device

    has_target, num_values = tcme.has_target, tcme.num_values

    status = dev.read_status()
    state = status.STATE

    value = dev.read_value()
    assert len(value) == num_values

    limits = dev.get_limits()
    for v in value:
        assert limits[0] <= v <= limits[1]

    if not has_target:
        with pytest.raises(ApiError):
            dev.read_target()
        with pytest.raises(ApiError):
            dev.change_target(value)
        return

    target = dev.read_target()
    for t in target:
        assert limits[0] <= t <= limits[1]
    if target == value:
        assert state in [PLCStatus.IDLE, PLCStatus.DISABLED,
                         PLCStatus.WARN]
    else:
        assert state in [PLCStatus.DISABLED, PLCStatus.START,
                         PLCStatus.BUSY, PLCStatus.STOP, PLCStatus.ERROR]


def test_flat_device(plc_flat_device):
    """test flat parameter access"""
    # zapf-device, TYPCODE_MAP entry
    dev, tcme = plc_flat_device

    # check param access to UserMin
    v = dev.get_param('UserMin')[1]
    dev.set_param('UserMin', v+1)
    assert v+1 == dev.get_param('UserMin')[1]
    dev.set_param('UserMin', v)

    assert tcme.num_params == len(dev.list_params())

    # check param access of all other params
    for p in dev.list_params():
        print(p)
        if p == 'UserMin':
            continue
        v = dev.get_param(p)[1]
        dev.set_param(p, v+1)
        assert v+1 == dev.get_param(p)[1]
        dev.set_param(p, v)


def test_paramif(plc_param_device):
    """test paramif access + funcs"""
    # zapf-device, TYPCODE_MAP entry
    dev, _tcme = plc_param_device

    # testplc implements a few parameters:
    # readable: 1-3, 32-38, 40, 43, 44, 51-53, 55-65, 68-70
    # writeable: 32-37, 40, 51-53, 56, 57, 60, 61, 69, 70
    # executable: 128, 133, 137, 142
    # 128 and 133 almost instantly go from BUSY to DONE, rest is ERR_RETRY

    # check state machine
    dev.update_param_sm()
    assert dev.param_sm.CMD != 0

    # basic lowlevel tests

    # set a known paramvalue != 0 first
    dev.set_param_value(1, 1)
    # initiate reading parameter 1 (should result in value 0)
    dev.set_param_cmd(ParamCMDs.DO_READ, 0, 1)
    assert dev.wait_sm_available()
    assert dev.param_sm.CMD == ParamCMDs.DONE
    assert dev.get_param_value(1) == 0

    # try to read param 127 (should fail with NO_IDX)
    assert dev.wait_sm_available()
    dev.set_param_cmd(ParamCMDs.DO_READ, 0, 127)
    assert dev.wait_sm_available()
    assert dev.param_sm.CMD == ParamCMDs.ERR_NO_IDX

    # try to write param 1 (should fail with RO)
    assert dev.wait_sm_available()
    dev.set_param_value_and_cmd(ParamCMDs.DO_WRITE, 0, 1, 42)
    assert dev.wait_sm_available()
    assert dev.param_sm.CMD == ParamCMDs.ERR_RO

    # try to exec func 142 (should fail with RETRY)
    assert dev.wait_sm_available()
    dev.set_param_cmd(ParamCMDs.DO_WRITE, 0, 142)
    assert dev.wait_sm_available()
    assert dev.param_sm.CMD == ParamCMDs.ERR_RETRY

    # try to 'BUSY' param 1 (should succeed with DONE)
    assert dev.wait_sm_available()
    dev.set_param_value_and_cmd(ParamCMDs.BUSY, 0, 1, 42)
    assert dev.wait_sm_available()
    assert dev.param_sm.CMD == ParamCMDs.DONE
    assert dev.get_param_value(1) != 42

    # higher level tests
    if 'UserMax' in dev.list_params():
        v = dev.get_param('UserMax')[1]
        dev.set_param('UserMax', v + 1)
        assert dev.get_param('UserMax')[1] == v + 1

    if dev.list_funcs():
        dev.exec_func(dev.list_funcs()[0])
