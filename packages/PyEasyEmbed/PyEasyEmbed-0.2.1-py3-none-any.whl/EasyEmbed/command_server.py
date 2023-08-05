from typing import Callable
import sys
import json
import traceback

class CliCommandServer():

    def _load_argv(self):
        self.argv = sys.argv

    def __init__(self, version: str = "1.0.0", strict: bool = True):
        self.commands = {"info": self.info}
        self.strict = strict
        self.version = version

    def info(self, data):
        return {
            "data_echo": data,
            "version": self.version,
            "python_version": sys.version,
            "data_strict": self.strict,
        }

    def command(self, func: Callable):
        self.commands[func.__name__] = func
        def wrapper(*args, **kwargs):
            func()
        return wrapper

    def _execute(self):
        self._load_argv()
        if len(self.argv) < 2:
            return {
                "status": -2,
                "message": "Command missing!"
            }
        command = self.argv[1]
        try:
            if self.strict:
                data_raw = self.argv[2]
            else:
                data_raw = " ".join(self.argv[2:])
            data = json.loads(data_raw)
        except IndexError:
            data = None
        except json.decoder.JSONDecodeError:
            return {
                "status": -3,
                "message": "JSON data could not be parsed!"
            }
        if command in self.commands:
            try:
                res = self.commands[command](data)
                if type(res) == bytes:
                    return res
                return {
                    "status": 0,
                    "response": res
                }
            except:
                tb = traceback.format_exc()
                return {
                    "status": 1,
                    "message": "Exception occured while executing command!",
                    "exception": tb
                }
        else:
            return {
                "status": -1,
                "message": "Command does not exist!"
            }
    
    def execute(self):
        print(json.dumps(self._execute()))
        