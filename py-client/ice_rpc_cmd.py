from enum import Enum
import sys
import argparse
import cmd2
import Home

INTRO = 'Smart Home RPC remote controller\nv0.1 2020\n'
PROMPT = 'Home> '


class DeviceCategory(Enum):
    home = 1
    wall_camera = 2
    drone_camera = 3
    grass_mower = 4
    fridge = 5


def device_name_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=True, action='store', help='Name of the device to access')
    return parser


class RpcController:
    def __init__(self, communicator, server_cmd):
        self.communicator = communicator
        self.server_cmd = server_cmd
        self.proxies = {}

    def access_object(self, name, category):
        identity = '{}/{}'.format(category.name, name)
        if identity not in self.proxies:
            self.proxies[identity] = self.__get_object_access(identity, category)
        return self.proxies[identity]

    def __get_object_access(self, identity, category):
        print("Attempt to access new object: " + identity)
        proxy = self.communicator.stringToProxy(identity + ':' + self.server_cmd)
        obj = None
        if category == DeviceCategory.home:
            obj = Home.HomeStatusPrx.checkedCast(proxy)
        elif category == DeviceCategory.wall_camera:
            obj = Home.Garden.WallCameraControllerPrx.checkedCast(proxy)
        elif category == DeviceCategory.drone_camera:
            obj = Home.Garden.DroneCameraControllerPrx.checkedCast(proxy)
        elif category == DeviceCategory.grass_mower:
            obj = Home.Garden.GrassMowerControllerPrx.checkedCast(proxy)
        elif category == DeviceCategory.fridge:
            obj = Home.Kitchen.FridgeControllerPrx.checkedCast(proxy)
        if not obj:
            raise RuntimeError('Failed to access object')
        return obj


class DeviceCmd(cmd2.Cmd):
    prompt = PROMPT

    def __init__(self, communicator, server_cmd):
        self.communicator = communicator
        self.server_cmd = server_cmd
        self.controller = RpcController(communicator, server_cmd)
        super().__init__()

    def cmdloop(self, intro=INTRO):
        return cmd2.Cmd.cmdloop(self, intro)

    @cmd2.with_argparser(device_name_parser())
    def do_list_devices(self, args):
        """List all currently available and instantiated devices."""
        proxy = self.controller.access_object(args.name, DeviceCategory.home)
        print(proxy.getActiveDevices())

    @staticmethod
    def do_exit(args):
        """Exit the program"""
        sys.exit(0)
