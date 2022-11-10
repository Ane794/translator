import pyperclip

from ._input import _Input


class Input(_Input):
    def input(self):
        return pyperclip.paste()
