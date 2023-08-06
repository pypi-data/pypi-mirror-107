from typing import List


class IMultilineParser:

    @property
    def key_name(self) -> str:
        raise NotImplementedError

    def parse(self, multiline_buffer: str) -> List[dict]:
        raise NotImplementedError

    def assemble(self, lines_data: List[dict]) -> List[str]:
        raise NotImplementedError
