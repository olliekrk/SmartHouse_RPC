import sys
from enum import Enum

import cmd2

import Home
import ice_parsers

INTRO = 'Smart Home RPC remote controller\nv0.1 2020\n'
PROMPT = 'Home> '


class DeviceCategory(Enum):
    home = 1
    wall_camera = 2
    drone_camera = 3
    grass_mower = 4
    fridge = 5


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

    @cmd2.with_argparser(ice_parsers.device_name_parser())
    def do_list_devices(self, args):
        """List all currently available and instantiated devices."""
        proxy = self.controller.access_object(args.name, DeviceCategory.home)
        print(proxy.getActiveDevices())

    @cmd2.with_argparser(ice_parsers.grass_mower_parser())
    def do_grass_mower(self, args):
        """Control the grass mowers"""
        proxy = self.controller.access_object(args.name, DeviceCategory.grass_mower)
        if args.get_coords:
            print(proxy.getCoordinates())
        elif args.set_coords:
            if args.x is not None and args.y is not None:
                try:
                    proxy.setCoordinates(Home.Garden.Coordinates(args.x, args.y))
                except Home.HomeException as e:
                    print('Unable to proceed!: ', str(e))
            else:
                print('Coordinates were not provided')
        elif args.on:
            proxy.turnSwitch(True)
        elif args.off:
            proxy.turnSwitch(False)

    @cmd2.with_argparser(ice_parsers.wall_camera_parser())
    def do_wall_camera(self, args):
        """Control the wall cameras"""
        proxy = self.controller.access_object(args.name, DeviceCategory.wall_camera)
        if args.is_visible:
            print(proxy.isVisible())
        elif args.visible:
            print(proxy.setVisibility(True))
        elif args.invisible:
            print(proxy.setVisibility(False))
        else:
            self.__dispatch_camera(args, proxy)

    @cmd2.with_argparser(ice_parsers.drone_camera_parser())
    def do_drone_camera(self, args):
        """Control the flying drone cameras"""
        proxy = self.controller.access_object(args.name, DeviceCategory.drone_camera)
        if args.get_altitude:
            print(proxy.getAltitude())
        elif args.set_altitude is not None:
            try:
                proxy.setAltitude(args.set_altitude)
            except Home.HomeException as e:
                print('Unable to proceed!: ', str(e))
        else:
            self.__dispatch_camera(args, proxy)

    @cmd2.with_argparser(ice_parsers.fridge_parser())
    def do_fridge(self, args):
        """Control the smart fridge"""
        proxy = self.controller.access_object(args.name, DeviceCategory.fridge)
        if args.message_of_the_day:
            print(proxy.getMessageOfTheDay())
        elif args.get_temperature:
            print(proxy.getTemperature())
        elif args.get_items:
            print(proxy.getItems())
        elif args.eco_on:
            proxy.setEcoMode(True)
        elif args.eco_off:
            proxy.setEcoMode(False)
        elif args.set_temperature:
            value = args.temperature_value
            unit = args.temperature_unit
            if value is not None and unit is not None:
                try:
                    proxy.setTemperature(Home.Kitchen.Temperature(Home.TemperatureUnit[unit], value))
                except Home.HomeException as e:
                    print("Unable to proceed!: ", str(e))
            else:
                print("Temperature unit and value parameters must be provided")
        elif args.put_items:
            if args.quantity is not None and args.item_name is not None:
                try:
                    proxy.putItems(Home.Kitchen.Item(args.item_name, args.quantity))
                except Home.HomeException as e:
                    print("Unable to proceed!: ", str(e))
            else:
                print("Item name and quantity parameters must be provided")
        elif args.remove_items:
            if args.quantity is not None and args.item_name is not None:
                try:
                    proxy.removeItems(Home.Kitchen.Item(args.item_name, args.quantity))
                except Home.HomeException as e:
                    print("Unable to proceed!: ", str(e))
            else:
                print("Item name and quantity parameters must be provided")

    @staticmethod
    def __dispatch_camera(args, proxy):
        if args.get_zoom:
            print(proxy.getZoom())
        elif args.zoom_in is not None:
            proxy.zoomIn(args.zoom_in)
        elif args.zoom_out is not None:
            proxy.zoomOut(args.zoom_in)
        elif args.get_direction:
            print(proxy.getDirection())
        elif args.set_direction is not None:
            proxy.setDirection(Home.Direction[args.set_direction])
        elif args.get_coords:
            print(proxy.getCoordinates())
        elif args.set_coords:
            if args.x is not None and args.y is not None:
                try:
                    proxy.setCoordinates(Home.Garden.Coordinates(args.x, args.y))
                except Home.HomeException as e:
                    print('Unable to proceed!: ', str(e))
            else:
                print('Coordinates were not provided')

    @staticmethod
    def do_exit(_args):
        """Exit the program"""
        sys.exit(0)
