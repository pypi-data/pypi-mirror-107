from .command_server import CliCommandServer
from bottle import Bottle, request, response
import json
import urllib

class HttpCommandServer(CliCommandServer):
    http_app = Bottle()
    def _load_argv(self):
        body = request.body.read()
        body = body.replace(b"+",b"").replace(b"payload=",b"")
        if body == b'':
            self.argv = [None, request.current_command]
        else:
            self.argv = [None, request.current_command, body.decode('utf8')]
        
    
    def __init__(self, version: str = "1.0.0", strict: bool = True):
        super().__init__(version=version, strict=strict)
        self.http_app.route("/<command>", "POST", self._execute)
    
    @http_app.error(404)
    def _error_404(self):
        return json.dumps({
            "status": -1,
            "message": "Command does not exist!"
        }, separators=(',', ':'))

    def _execute(self, command):
        request.current_command = command
        return super()._execute()
    
    def execute(self, port = 43512, debug = False, server = "wsgiref"):
        self.http_app.run(host = "localhost", port = port, debug = debug, server = server)
