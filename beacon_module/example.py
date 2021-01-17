"""
example.py

created by dromakin as 30.12.2020
Project Ibacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201230'

# Works
# bluetooth low energy scan
# import asyncio
# from bleak import BleakScanner
#
#
# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

# import asyncio
# from bleak import BleakScanner
#
# async def run():
#     async with BleakScanner() as scanner:
#         await asyncio.sleep(5.0)
#         devices = await scanner.get_discovered_devices()
#     for d in devices:
#         print(d)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())


import asyncio
from bleak import BleakScanner
import time


def get_metres_from_rssi(device,): # rssi: int = None, txpower: int = None):
    default_measure_power = -69
    N = 2.3  # 2-4 dbm
    distance = None

    rssi = device.rssi
    txpower = device.details.get('TxPower')

    # if rssi == None:
    #     for i in range(5):
    #         rssi1 = device.details.get('RSSI')
    #         rssi2 = device.rssi
    #         if rssi1 != None:
    #             rssi = rssi1
    #             break
    #         elif rssi2 != None:
    #             rssi = rssi2
    #             break
    #         else:
    #             time.sleep(1)
    #
    # if rssi == None:
    #     return "No rssi"
    # if device.name == "69-B6-E2-F0-A7-A1" or device.name == "63-D9-6C-2D-9B-61" or device.name == "SberBox":
    #     print()
    #     print(rssi, txpower)
    #     print()

    if txpower == None and rssi <= 0:
        distance = 10 ** ((default_measure_power - rssi) / (10 * N))
        return distance

    if txpower == None and rssi >= 0:
        distance = 10 ** ((default_measure_power - (-1 * rssi)) / (10 * N))
        return distance

    # Filtering anomaly metrics
    if txpower < 5 and txpower >= 0 and rssi <= 0:
        distance = 10 ** ((default_measure_power - rssi) / (10 * N))
        return distance

    if txpower < 5 and txpower >= 0 and rssi >= 0:
        distance = 10 ** ((default_measure_power - (-1 * rssi)) / (10 * N))
        return distance

    # Normal metrics
    if rssi <= 0 and txpower <= 0:
        distance = 10 ** ((txpower - rssi) / (10 * N))
        return distance

    if rssi >= 0 and txpower >= 0:
        distance = 10 ** (((-1 * txpower) - (-1 * rssi)) / (10 * N))
        return distance

    if rssi >= 0 and txpower <= 0:
        distance = 10 ** ((txpower - (-1 * rssi)) / (10 * N))
        return distance

    if rssi <= 0 and txpower >= 0:
        distance = 10 ** (((-1 * txpower) - rssi) / (10 * N))
        return distance

    return distance

    # if txpower is None:
    #     if rssi < 0:
    #         return 10 ** ((default_measure_power - rssi) / (10 * N))
    #     elif rssi > 0:
    #         return 10 ** ((default_measure_power - (-1 * rssi)) / (10 * N))
    # else:
    #     if rssi < 0 and txpower < 0:
    #         return 10 ** ((txpower - rssi) / (10 * N))
    #
    #     elif rssi > 0 and txpower > 0:
    #         return 10 ** (((-1 * txpower) - (-1 * rssi)) / (10 * N))

    # print("no rssi")
    # return None


def detection_callback(device, advertisement_data):
    # print(device.address, "RSSI:", device.rssi, advertisement_data)
    # print(f"Name: {device.name}, Address: {device.address}, rssi: {device.rssi}, details: {device.details}, manufacturer_data_76: {advertisement_data.manufacturer_data}")
    # print(f"Name: {device.name}, Address: {device.address}, rssi: {device.rssi}, manufacturer_data_76: {advertisement_data.manufacturer_data.get(76).decode('cp1251').encode('utf8')}")
    # print(f"Name: {device.name}, Address: {device.address}, rssi: {device.rssi}, details: {device.details}")
    # get_metres_from_rssi
    # txpower = device.details.get('TxPower')
    # rssi = device.details.get('RSSI')
    # if rssi is None:
    #     rssi = device.rssi
    # if rssi is None:
    #     print(f"No rssi for name: {device.name}, Address: {device.address}")
    # else:
    #     print(f"Name: {device.name}, Address: {device.address}, rssi: {device.rssi}, metres: {get_metres_from_rssi(int(rssi), txpower)}")

    name = device.name
    address = device.address
    rssi = device.rssi
    print(type(rssi))

    print(name, address, rssi, end=" ")

    txpower = device.details.get('TxPower')
    print(txpower, end=" ")
    metres = get_metres_from_rssi(device,) # int(rssi), txpower)
    print(metres)


async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()
    # devices = await scanner.get_discovered_devices()

    # for d in devices:
    #     print(d)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


# async def run():
#     scanner = BleakScanner()
#     scanner.register_detection_callback(detection_callback)
#     await scanner.start()
#     await asyncio.sleep(5.0)
#     await scanner.stop()
#     # devices = await scanner.get_discovered_devices()
#
#     # for d in devices:
#     #     print(d)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

# Works
# import gatt
#
# class AnyDeviceManager(gatt.DeviceManager):
#     def device_discovered(self, device):
#         print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))
#
# manager = AnyDeviceManager(adapter_name='hci0')
# manager.start_discovery()
# manager.run()

# import time
#
# from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement, BluetoothAddressType
#
# def callback(bt_addr, rssi, packet, additional_info):
#     print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
#
# # scan for all iBeacon advertisements from beacons with certain properties:
# # - uuid
# # - major
# # - minor
# # at least one must be specified.
# scanner = BeaconScanner(
#     callback,
#     scan_parameters={"address_type": BluetoothAddressType.PUBLIC}
# )
# scanner.start()
# time.sleep(60)
# scanner.stop()
#
# # scan for all iBeacon advertisements regardless from which beacon
# scanner = BeaconScanner(callback,
#     packet_filter=IBeaconAdvertisement
# )
# scanner.start()
# time.sleep(60)
# scanner.stop()
