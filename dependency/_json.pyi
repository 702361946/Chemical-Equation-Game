#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)


class Json(object):
    def __init__(
            self,
            file_path: str = 'json',
            encoding: str = 'utf-8',
            indent: int = 4,
            ensure_ascii: bool = False
    ) -> object:
        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        ...

    def dump(self, a, file_name: str, file_path: list[str] | str = None) -> bool:
        ...

    def load(self, file_name: str, file_path: list[str] | str = None):
        ...

    def logging_get(self) -> None:
        ...
