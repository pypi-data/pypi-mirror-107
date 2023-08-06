
from typing import List
from xscreensaver_config.multiline_parser.IMultilineParser import IMultilineParser
from xscreensaver_config.multiline_parser.ProgramsParser import ProgramsParser


class ConfigParser:
    multiline = False
    multiline_key = None
    multiline_buffer = ''
    data = {}
    multiline_parsers_by_key = {}

    def __init__(self, config_path, multiline_parsers: List[IMultilineParser] = None, app_name: str = 'xscreensaver config parser', ignore_missing_file: bool = False):
        self.config_path = config_path
        self.multiline_parsers = multiline_parsers if multiline_parsers else [ProgramsParser()]
        self.app_name = app_name

        for multiline_parser in self.multiline_parsers:
            if not isinstance(multiline_parser, IMultilineParser):
                raise Exception('{} is not instance of IMultilineParser'.format(multiline_parser))
            self.multiline_parsers_by_key[multiline_parser.key_name] = multiline_parser
        try:
            self._load()
        except FileNotFoundError:
            if not ignore_missing_file:
                raise

    def _end_multiline(self):
        if self.multiline:
            found_parser = self.multiline_parsers_by_key.get(self.multiline_key)
            if found_parser:
                self.data[self.multiline_key] = found_parser.parse(self.multiline_buffer)
            else:
                self.data[self.multiline_key] = self.multiline_buffer
            self.multiline = False
            self.multiline_key = None
            self.multiline_buffer = ''

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
                    self.multiline_buffer += line.rstrip().rstrip('\\')
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
                    assembled_multiline = found_parser.assemble(value)
                    lines.extend(self._wrap_multiline(assembled_multiline))
                    lines.append('')
                    lines.append('')
            else:
                lines.append('{}: {}'.format(key, value))
        return lines

    def _wrap_multiline(self, multiline: List[str], width: int = 50) -> List[str]:
        wrapped_lines = []
        for line in multiline:
            if len(line) > width:
                splited = [line[i:i+width] for i in range(0, len(line), width)]
                wrapped_lines.extend(splited)
            else:
                wrapped_lines.append(line)

        return [wl + '\\' for wl in wrapped_lines]

    def write(self, config_path: str):
        with open(config_path, 'w') as w:
            w.writelines(['{}\n'.format(a) for a in self._assemble()])

    def read(self):
        return self.data

    def update(self, data: dict):
        self.data.update(data)

    def save(self):
        self.write(self.config_path)
