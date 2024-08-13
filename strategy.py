from abc import ABC, abstractmethod


class FileProcessStrategy:
    def get_window_title(self) -> str:
        raise NotImplementedError

    def get_file_types(self) -> list:
        raise NotImplementedError

    def get_command_name(self):
        raise NotImplementedError

    def run(self, files) -> None:
        raise NotImplementedError