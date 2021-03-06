from datetime import datetime
import os
import json


class Logger:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def save(self, content: str) -> bool:
        arg = "w"
        if os.path.isfile(self.filename):
            arg = "a"
        with open(self.filename, arg) as f:
            f.write(str(content) + "\n")

    def info(self, content: str) -> None:
        out = datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " [INFO] " + content
        print(out, flush=True)
        self.save(out)

    def error(self, content: str) -> None:
        out = datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " [ERROR] " + content
        print(out, flush=True)
        self.save(out)


# def jsonify_quotes(filename):
#   with open(filename, "r") as f:
#       x = f.read()
#       y = x.split(": ")
#       name = y[0]
#       token = y[1]
#       return {
#           name.split("{")[1].strip(): token.split("}")[0].strip()
#       }


def load(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())
