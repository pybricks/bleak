"""
Perform Bluetooth LE Scan.

macOS

Created on 2019-06-24 by kevincar <kevincarrolldavis@gmail.com>

"""

import asyncio
from typing import List

from bleak.backends.corebluetooth import CBAPP as cbapp
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError

_manager = cbapp.central_manager_delegate

async def discover(timeout: float = 5.0, **kwargs) -> List[BLEDevice]:
    """Perform a Bluetooth LE Scan.

    Args:
        timeout (float): duration of scanning period

    """
    try:
        await _manager.waitForPowerOn_(0.1)
    except asyncio.TimeoutError:
        raise BleakError("Bluetooth device is turned off")

    scan_options = {"timeout": timeout}

    await _manager.scanForPeripherals_(scan_options)

    # CoreBluetooth doesn't explicitly use MAC addresses to identify peripheral
    # devices because private devices may obscure their MAC addresses. To cope
    # with this, CoreBluetooth utilizes UUIDs for each peripheral. We'll use
    # this for the BLEDevice address on macOS

    devices = _manager.devices
    return list(devices.values())
