# Copyright 2019 Nokia

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import sys
import inspect
import etcd


class VerboseLogger(object):
    def __call__(self, msg):
        print(msg)


class CLIHandler(object):
    def __init__(self):
        self.sock = None
        self.verbose_logger = VerboseLogger()
        self.client = None

    def _init_api(self, server, port, verbose):
        logger = None
        if verbose:
            logger = self.verbose_logger

        if server == 'none':
            import socket
            server = socket.gethostname()

        self.client = etcd.Client(server, port)

    def set_handler(self, subparser):
        subparser.set_defaults(handler=self)

    def init_subparser(self, subparsers):
        raise Error('Not implemented')

    def __call__(self, args):
        raise Error('Not implemented')


class CLILockHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('lock', help='Acquire a lock')
        subparser.add_argument('--id',
                               required=True,
                               dest='id',
                               metavar='ID',
                               type=str,
                               action='store')

        subparser.add_argument('--timeout',
                               required=True,
                               dest='timeout',
                               metavar='TIMEOUT',
                               type=int,
                               action='store')

        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.port, args.verbose)
        lock = etcd.Lock(self.client, args.id)
        result = lock.acquire(blocking=True, lock_ttl=args.timeout)
        if not result:
            raise Exception('Lock taken!')

        print('Lock acquired successfully!')
        print('uuid=%s' % lock.uuid)

class CLIUnlockHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('unlock', help='Release a lock')
        subparser.add_argument('--id',
                               required=True,
                               dest='id',
                               metavar='ID',
                               type=str,
                               action='store')

        subparser.add_argument('--uuid',
                               required=True,
                               dest='uuid',
                               metavar='UUID',
                               type=str,
                               action='store')
        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.port, args.verbose)
        lock = etcd.Lock(self.client, args.id)
        try:
            lock._uuid = args.uuid
            lock.release()
            print('Lock released successfully!')
        except ValueError:
            print('Lock is not held!')

def get_handlers_list():
    handlers = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if name is not 'CLIHandler':
                if issubclass(obj, CLIHandler):
                    handlers.append(obj())
    return handlers


def main():
    handlers = get_handlers_list()
    for handler in handlers:
        print('handler is ', handler)


if __name__ == '__main__':
    main()
