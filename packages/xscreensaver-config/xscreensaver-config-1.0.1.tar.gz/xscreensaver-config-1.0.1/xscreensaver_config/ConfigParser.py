
from typing import List
from xscreensaver_config.multiline_parser.IMultilineParser import IMultilineParser
from xscreensaver_config.multiline_parser.ProgramsParser import ProgramsParser


class ConfigParser:
    multiline = False
    multiline_key = None
    multiline_buffer = []
    data = {}
    multiline_parsers_by_key = {}

    def __init__(self, config_path, multiline_parsers: List[IMultilineParser] = None, app_name: str = 'xscreensaver config parser'):
        self.config_path = config_path
        self.multiline_parsers = multiline_parsers if multiline_parsers else [ProgramsParser()]
        self.app_name = app_name

        for multiline_parser in self.multiline_parsers:
            if not isinstance(multiline_parser, IMultilineParser):
                raise Exception('{} is not instance of IMultilineParser'.format(multiline_parser))
            self.multiline_parsers_by_key[multiline_parser.key_name] = multiline_parser

        self._load()

    def _end_multiline(self):
        if self.multiline:

            found_parser = self.multiline_parsers_by_key.get(self.multiline_key)

            if found_parser:
                self.data[self.multiline_key] = found_parser.parse(self.multiline_buffer)
            else:
                self.data[self.multiline_key] = self.multiline_buffer
            self.multiline = False
            self.multiline_key = None
            self.multiline_buffer = []

    def _load(self):
        with open(self.config_path, 'r') as r:
            self._parse(r.readlines())

    def _parse(self, lines: List[str]):
        for line in lines:
            if not line.strip():
                self._end_multiline()
                continue
            if line.startswith('#'):
                self._end_multiline()
                continue

            if not self.multiline:
                try:
                    key, value = line.split(':', 1)
                    if line.strip().endswith('\\'):
                        self.multiline = True
                        self.multiline_key = key
                except ValueError:
                    raise Exception('Failed to parse line {}'.format(line))

                self.data[key.strip(':')] = value.strip()
            else:
                if line.strip().endswith('\\'):
                    self.multiline_buffer.append(line.rstrip())
                else:
                    self._end_multiline()

    def _assemble(self) -> List[str]:
        lines = [
            '# XScreenSaver Preferences File',
            '# Written by {}.'.format(self.app_name),
            '# https://github.com/Salamek/chromium-kiosk',
            ''
        ]
        for key, value in self.data.items():
            if isinstance(value, list):
                lines.append('{}: {}'.format(key, '\\'))
                found_parser = self.multiline_parsers_by_key.get(key)
                if found_parser:
                    lines.extend(found_parser.assemble(value))
            else:
                lines.append('{}: {}'.format(key, value))
        return lines

    def _write(self, config_path: str):
        with open(config_path, 'w') as w:
            w.writelines(['{}\n'.format(l) for l in self._assemble()])

    def read(self):
        return self.data

    def update(self, data: dict):
        self.data.update(data)

    def save(self):
        self._write(self.config_path)
