import re
from typing import List
from xscreensaver_config.multiline_parser.IMultilineParser import IMultilineParser


class ProgramsParser(IMultilineParser):
    key_name = 'programs'

    def _parse_line(self, line: str) -> dict:
        regex = re.compile(r'^(-|)(?:\s+|)(\S+:|)(?:\s+|)\t{4}(.+?)\s+$')
        found = regex.match(line)
        if not found:
            raise Exception('Failed to parse line {}'.format(line))
        return {
            'enabled': found.group(1) != '-',
            'renderer': found.group(2).rstrip(':'),
            'command': found.group(3)
        }

    def _assemble_line(self, line_data: dict) -> str:
        parts = []
        if not line_data.get('enabled'):
            parts.append('-')

        if line_data.get('renderer'):
            if line_data.get('enabled'):
                parts.append(' ')
            parts.append(' {}: '.format(line_data.get('renderer')))

        parts.append('\t\t\t\t')
        parts.append(line_data.get('command'))
        parts.append('\t\t\t    \\n')

        return ''.join(parts)

    def parse(self, multiline_buffer: str) -> List[dict]:
        # join lines into single string and unescape it and parse lines again
        lines = multiline_buffer.encode('UTF-8').decode('unicode_escape').splitlines()
        parsed_lines = [self._parse_line(line) for line in lines]

        if len(lines) != len(parsed_lines):
            raise Exception('Parsing failed, lines {}!={}'.format(len(lines), len(parsed_lines)))

        return parsed_lines

    def assemble(self, lines_data: List[dict]) -> List[str]:
        return [self._assemble_line(line_data) for line_data in lines_data]
