from ._output import _Output


class Output(_Output):
    def output(self, msg: str):
        print(msg)
