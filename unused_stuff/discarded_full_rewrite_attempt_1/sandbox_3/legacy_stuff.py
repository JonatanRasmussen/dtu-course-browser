from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type, Callable, TypeVar, Generic
import json

from choose_love import DataObject

T = TypeVar('T')

class DAO(Generic[T]):

    def __init__(self) -> None:
        self.dct: Dict[str, T] = {}

    def exists(self, key: str) -> bool:
        return key in self.dct

    def read(self, key: str) -> T:
        self._raise_error_if_key_missing(key)
        return self.dct[key]

    def write_unique_key(self, key: str, value: T) -> None:
        self._raise_error_if_key_exists(key)
        self._write(key, value)

    def write_if_key_missing(self, key: str, value: T) -> None:
        if not self.exists(key):
            self._write(key, value)

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value

    def _raise_error_if_key_exists(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exist.")

    def _raise_error_if_key_missing(self, key: str) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists.")

class DiskAccess(DAO,Generic[T]):

    FILE_PATH: str = "json_files/"
    FILE_NAME: str = "parsed_data"

    def __init__(self) -> None:
        super().__init__()
        self.file_path: str = f"{DiskAccess.FILE_PATH}{DiskAccess.FILE_NAME}.json"
        self._load_from_disk()

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value
        self._save_to_disk()

    def _load_from_disk(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as json_file:
                self.dct = json.load(json_file)
        except FileNotFoundError:
            self.dct = {}

    def _save_to_disk(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.dct, json_file, indent=4)

dao: DAO = DAO[DataObject]()
child_lists: DiskAccess = DiskAccess[List[str]]()
data_dicts: DiskAccess = DiskAccess[Dict[str,str]]()