import argparse
import Home


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
    exclusive_actions.add_argument('-invisible', action='store_true', help='Hide this camera')
    return parser


def drone_camera_parser():
    parser, exclusive_actions, arguments = camera_parser_base()
    exclusive_actions.add_argument('-get_altitude', action='store_true', help='Get drone altitude')
    exclusive_actions.add_argument('-set_altitude', action='store', type=float, help='Set drone altitude')
    return parser


def fridge_parser():
    parser, exclusive_actions, arguments = device_with_args_parser_base()
    exclusive_actions.add_argument('-set_temperature', action='store_true',
                                   help='Set temperature')
    exclusive_actions.add_argument('-get_temperature', action='store_true',
                                   help='Get current temperature')
    exclusive_actions.add_argument('-get_items', action='store_true',
                                   help='Check what items are currently in the fridge')
    exclusive_actions.add_argument('-put_items', action='store_true',
                                   help='Remotely order & put given number of items in the fridge')
    exclusive_actions.add_argument('-remove_items', action='store_true',
                                   help='Remotely remove given number of items from the fridge')
    exclusive_actions.add_argument('-eco_off', action='store_true',
                                   help='Disable the eco mode of this fridge')
    exclusive_actions.add_argument('-eco_on', action='store_true',
                                   help='Enable the eco mode of this fridge')
    exclusive_actions.add_argument('-motd', '--message_of_the_day', action='store_true',
                                   help='Get the Message Of The Day, and check ECO-MODE settings')
    arguments.add_argument('-q', '--quantity', action='store', type=int, help='Quantity of items to put or remove')
    arguments.add_argument('-item', '--item_name', action='store', type=str, help='Name of item to put or remove')
    arguments.add_argument('-t', '--temperature-value', action='store', type=float, help='Temperature value')
    arguments.add_argument('-u', '--temperature-unit', action='store', help='Temperature unit',
                           choices=[Home.TemperatureUnit.Celsius.name, Home.TemperatureUnit.Fahrenheit.name])
    return parser
