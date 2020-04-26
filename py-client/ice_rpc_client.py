import sys

import Ice

from ice_rpc_cmd import DeviceCmd

SERVER_PORT_CMD = 'tcp -h localhost -p 10000'


def run():
    with Ice.initialize(sys.argv) as communicator:
        DeviceCmd(communicator, SERVER_PORT_CMD).cmdloop()


if __name__ == '__main__':
    print('Starting the client...')
    run()
