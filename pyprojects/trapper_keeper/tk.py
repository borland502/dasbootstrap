import contextlib
from enum import StrEnum, auto
from pathlib import Path

from trapper_keeper.stores.bolt_kvstore import BoltStore
from trapper_keeper.stores.keepass_store import KeepassStore


class DbTypes(StrEnum):
  BOLT: str = auto()
  KP: str = auto()
  SQLITE: str = auto()


def open_tk_store(db_type: DbTypes, db_path: Path, **kwargs) -> contextlib.AbstractContextManager:
  match db_type:
    case DbTypes.BOLT:
      readonly: bool = kwargs["readonly"]
      return BoltStore(bp_fp=db_path, readonly=readonly)
    case DbTypes.KP:
      key: Path = kwargs["key"]
      token: Path = kwargs["token"]
      return KeepassStore(kp_fp=db_path, kp_key=key, kp_token=token)
    case _:
      raise TypeError(f"Unknown db type {db_type}")
