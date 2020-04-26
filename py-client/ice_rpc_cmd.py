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


def grass_mower_parser():
    parser = device_name_parser()
    actions_group = parser.add_argument_group('actions')
    exclusive_actions_group = actions_group.add_mutually_exclusive_group()
    exclusive_actions_group.required = True
    exclusive_actions_group.add_argument('-get_coords', action='store_true', help='Get coordinates of this device')
    exclusive_actions_group.add_argument('-set_coords', action='store_true', help='Set coordinates of this device')
    exclusive_actions_group.add_argument('-on', action='store_true', help='Turn the engine ON')
    exclusive_actions_group.add_argument('-off', action='store_true', help='Turn the engine OFF')
    arguments_group = parser.add_argument_group('arguments')
    arguments_group.add_argument('-x', action='store', type=float, help='The X coordinate of the grass mower')
    arguments_group.add_argument('-y', action='store', type=float, help='The Y coordinate of the grass mower')
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

    @cmd2.with_argparser(grass_mower_parser())
    def do_grass_mower(self, args):
        """Control the grass mower"""
        proxy = self.controller.access_object(args.name, DeviceCategory.grass_mower)
        if args.set_coords:
            if args.x is not None and args.y is not None:
                try:
                    proxy.setCoordinates(Home.Garden.Coordinates(args.x, args.y))
                except Home.InvalidCoordinates as e:
                    print('InvalidCoordinates!: ', str(e))
            else:
                print('Coordinates were not provided')
        elif args.get_coords:
            print(proxy.getCoordinates())
        elif args.on:
            proxy.turnSwitch(True)
        elif args.off:
            proxy.turnSwitch(False)



    @staticmethod
    def do_exit(args):
        """Exit the program"""
        sys.exit(0)


"""
Drone Camera : get/set coordinates, direction, zoom, set altitude
Wall Camera : get/set coordinates, direction, zoom, set visibility
Fridge : get/set temperature, get motd, set eco mode, get items, add/remove items
"""
