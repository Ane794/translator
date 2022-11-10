import importlib
import threading
from time import sleep

from ruamel.yaml import YAML


class Translator:
    def __init__(self):
        self._config = {}

        self._input = None
        self._translate = None
        self._output = None

        self._parse_config()
        self._init_translator()

    def _parse_config(self, conf_url='config.yml'):
        with open(conf_url, 'r') as conf_file:
            self._config = YAML().load(conf_file)

    def _init_translator(self):
        _i = self._config.get('option').get('input')  # config.option.input
        _input = self._config.get('input')[_i]  # config.input[_i]

        _i = self._config.get('option').get('translate')  # config.option.translate
        _translate = self._config.get('translate')[_i]  # config.translate[_i]

        _i = self._config.get('option').get('output')  # config.option.output
        _output = self._config.get('output')[_i]  # config.output[_i]

        self._input = importlib.import_module(f'input.{_input.get("name")}') \
            .__getattribute__('Input')(_input) \
            .__getattribute__('input')

        self._translate = importlib.import_module(f'translate.{_translate.get("name")}') \
            .__getattribute__('Translate')(_translate) \
            .__getattribute__('translate')

        self._output = importlib.import_module(f'output.{_output.get("name")}') \
            .__getattribute__('Output')(_output) \
            .__getattribute__('output')

    def start(self):
        _string = ''

        def _duration_end():
            pass

        _t = threading.Timer(float(dict(self._config.get('option')).get('duration')), _duration_end)
        _t.start()
        while True:
            sleep(0.2)

            # 輸入.
            _input_content = self._input()

            if _input_content != _string:
                _string = _input_content
                while _t.is_alive():
                    pass

                # 翻譯並輸出.
                self._output(self._translate(_string))

                _t = threading.Timer(float(self._config.get('option').get('duration')), _duration_end)
                _t.start()


if __name__ == '__main__':
    Translator().start()
