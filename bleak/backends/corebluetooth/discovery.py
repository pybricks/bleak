"""
Perform Bluetooth LE Scan.

macOS

Created on 2019-06-24 by kevincar <kevincarrolldavis@gmail.com>

"""

import asyncio
from typing import List

from bleak.backends.corebluetooth.CentralManagerDelegate import CentralManagerDelegate
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError

async def discover(timeout: float = 5.0, **kwargs) -> List[BLEDevice]:
    """Perform a Bluetooth LE Scan.

    Args:
        timeout (float): duration of scanning period

    """
    manager = CentralManagerDelegate.alloc().init()
    try:
        await manager.waitForPowerOn_(0.1)
    except asyncio.TimeoutError:
        raise BleakError("Bluetooth device is turned off")

    manager.start_scan()
    await asyncio.sleep(timeout)
    manager.stop_scan()

    # CoreBluetooth doesn't explicitly use MAC addresses to identify peripheral
    # devices because private devices may obscure their MAC addresses. To cope
    # with this, CoreBluetooth utilizes UUIDs for each peripheral. We'll use
    # this for the BLEDevice address on macOS

    devices = manager.devices
    return list(devices.values())
