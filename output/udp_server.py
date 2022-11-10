import socket

from ._output import _Output


class Output(_Output):
    def output(self, msg: str):
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.sendto(msg.encode('UTF-8'), (self._config.get('host'), self._config.get('port')))
        _s.close()
