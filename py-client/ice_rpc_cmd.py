import argparse
import sys
from enum import Enum

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


def device_with_args_parser_base():
    parser = device_name_parser()
    actions_group = parser.add_argument_group('actions')
    arguments = parser.add_argument_group('arguments')
    exclusive_actions = actions_group.add_mutually_exclusive_group()
    exclusive_actions.required = True
    return parser, exclusive_actions, arguments


def coordinates_parser_base():
    parser, exclusive_actions, arguments = device_with_args_parser_base()
    exclusive_actions.add_argument('-get_coords', action='store_true', help='Get coordinates of this device')
    exclusive_actions.add_argument('-set_coords', action='store_true', help='Set coordinates of this device')
    arguments.add_argument('-x', action='store', type=float, help='The X coordinate of this device GPS system')
    arguments.add_argument('-y', action='store', type=float, help='The Y coordinate of this device GPS system')
    return parser, exclusive_actions, arguments


def camera_parser_base():
    parser, exclusive_actions, arguments = coordinates_parser_base()
    exclusive_actions.add_argument('-get_zoom', action='store_true', help='Get the current zoom of this camera')
    exclusive_actions.add_argument('-zoom_in', action='store', type=int, help='Zoom IN the camera lens.')
    exclusive_actions.add_argument('-zoom_out', action='store', type=int, help='Zoom OUT the camera lens.')
    exclusive_actions.add_argument('-get_direction', action='store_true', help='Get the direction the camera is facing')
    exclusive_actions.add_argument('-set_direction', action='store', help='Change the direction the camera is facing',
                                   choices=[Home.Direction.North.name,
                                            Home.Direction.East.name,
                                            Home.Direction.West.name,
                                            Home.Direction.South.name])
    return parser, exclusive_actions, arguments


def grass_mower_parser():
    parser, exclusive_actions, arguments = coordinates_parser_base()
    exclusive_actions.add_argument('-on', action='store_true', help='Turn the engine ON')
    exclusive_actions.add_argument('-off', action='store_true', help='Turn the engine OFF')
    return parser


def wall_camera_parser():
    parser, exclusive_actions, arguments = camera_parser_base()
    exclusive_actions.add_argument('-is_visible', action='store_true', help='Check if camera is in visible mode')
    exclusive_actions.add_argument('-visible', action='store_true', help='Set the camera to be visible')
    exclusive_actions.add_argument('-invisible', action='store_false', help='Hide this camera')
    return parser


def drone_camera_parser():
    parser, exclusive_actions, arguments = camera_parser_base()
    exclusive_actions.add_argument('-get_altitude', action='store_true', help='Get drone altitude')
    exclusive_actions.add_argument('-set_altitude', action='store', type=float, help='Set drone altitude')
    return parser


def fridge_parser():
    parser, exclusive_actions, arguments = device_with_args_parser_base()
    exclusive_actions.add_argument('-get_temperature', action='store_true',
                                   help='Get current temperature')
    exclusive_actions.add_argument('-get_items', action='store_true',
                                   help='Check what items are currently in the fridge')
    exclusive_actions.add_argument('-put_items', action='store_true',
                                   help='Remotely order & put given number of items in the fridge')
    exclusive_actions.add_argument('-remove_items', action='store_true',
                                   help='Remotely remove given number of items from the fridge')
    exclusive_actions.add_argument('-eco_mode', '--set_eco_mode', action='store', type=bool,
                                   help='Enable or disable the eco mode of this fridge')
    exclusive_actions.add_argument('-motd', '--message_of_the_day', action='store_true',
                                   help='Get the Message Of The Day, and check ECO-MODE settings')
    arguments.add_argument('-t', '--temperature-value', action='store', type=float, help='Temperature value')
    arguments.add_argument('-u', '--temperature-unit', action='store', help='Temperature unit',
                           choices=[Home.TemperatureUnit.Celsius.name, Home.TemperatureUnit.Fahrenheit.name])
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
        """Control the grass mowers"""
        proxy = self.controller.access_object(args.name, DeviceCategory.grass_mower)
        if args.set_coords:
            if args.x is not None and args.y is not None:
                try:
                    proxy.setCoordinates(Home.Garden.Coordinates(args.x, args.y))
                except Home.HomeException as e:
                    print('Unable to proceed!: ', str(e))
            else:
                print('Coordinates were not provided')
        elif args.get_coords:
            print(proxy.getCoordinates())
        elif args.on:
            proxy.turnSwitch(True)
        elif args.off:
            proxy.turnSwitch(False)

    @cmd2.with_argparser(wall_camera_parser())
    def do_wall_camera(self, args):
        """Control the wall cameras"""
        pass

    @cmd2.with_argparser(drone_camera_parser())
    def do_drone_camera(self, args):
        """Control the flying drone cameras"""
        pass

    @cmd2.with_argparser(fridge_parser())
    def do_fridge(self, args):
        """Control the smart fridge"""
        pass

    @staticmethod
    def do_exit(args):
        """Exit the program"""
        sys.exit(0)
