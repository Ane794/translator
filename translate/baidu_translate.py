import random
from hashlib import md5
from urllib.parse import urlencode

import requests

from ._translate import _Translate


class Translate(_Translate):
    def translate(self, _query) -> str:
        _salt = random.randint(0, 2147483647)
        _sign = md5(
            f'{self._config.get("appid")}{_query}{_salt}{self._config.get("key")}'
            .encode('UTF-8')
        ).hexdigest()
        _res = requests.get('https://fanyi-api.baidu.com/api/trans/vip/translate' + '?' + urlencode({
            'q': _query,
            'from': self._config.get('from'),
            'to': self._config.get('to'),
            'appid': self._config.get('appid'),
            'salt': _salt,
            'sign': _sign,
        })).json()

        _results = _res.get('trans_result', _res.get('error_msg'))
        _translated = ''
        if type(_results) is list:
            for _result in _results:
                _translated += _result.get('dst') + '\n'
        else:
            _translated = _results

        return _translated.strip()
