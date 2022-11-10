from urllib.parse import urlencode

import requests

from ._translate import _Translate


class Translate(_Translate):
    def __init__(self, _config: dict):
        super().__init__(_config)

        self._access_token = self._config.get('access_token')
        if not self._access_token:
            self._access_token = self._get_access_token()

    def translate(self, _query) -> str:
        _res = requests.post('https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1' + '?' + urlencode({
            'access_token': self._access_token,
            'q': _query,
            'from': self._config.get('from'),
            'to': self._config.get('to'),
            'term_ids': ','.join(str(_) for _ in self._config.get('term_ids'))
        })).json()

        _results = _res.get('result', _res.get('error_msg'))
        _translated = ''
        if type(_results) is dict:
            for _result in _results.get('trans_result'):
                _translated += _result.get('dst') + '\n'
        else:
            _translated = _results

        return _translated.strip()

    def _get_access_token(self) -> str:
        _res = requests.get('https://aip.baidubce.com/oauth/2.0/token' + '?' + urlencode({
            'grant_type': 'client_credentials',
            'client_id': self._config.get('api_key'),
            'client_secret': self._config.get('secret_key'),
        })).json()
        print(_res)
        return _res.get('access_token')
