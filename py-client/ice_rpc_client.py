import sys

import Ice
import Home

SERVER_PORT_CMD = 'tcp -h localhost -p 10000'


def identity_string(name, category=""):
    return '{}/{}'.format(category, name)


def run():
    with Ice.initialize(sys.argv) as communicator:
        identity = identity_string('Hello', 'home')
        print("Accessing object: " + identity)
        proxy = communicator.stringToProxy(identity + ':' + SERVER_PORT_CMD)
        obj = Home.HomeStatusPrx.checkedCast(proxy)
        print(dir(obj))
        if not obj:
            raise RuntimeError('Failed to access object reference')


if __name__ == '__main__':
    print('Starting the client')
    run()
