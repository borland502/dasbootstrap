"""Trapper Keeper interface to various DB Stores noted by class DbTypes."""

from __future__ import annotations

import contextlib
from enum import StrEnum, auto
from pathlib import Path

from dasbootstrap.trapper_keeper.stores.bolt_kvstore import BoltStore
from dasbootstrap.trapper_keeper.stores.keepass_store import KeepassStore
from pandas import DataFrame
from pykeepass.entry import Entry


# TODO: Factory pattern would probably suit here
class DbTypes(StrEnum):
  """Types of datastores that can be used.


  Args:
      StrEnum (_type_): String enum name of supported datastores.
  """

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


# TODO: Remove
def validate_tk_store(db_type: DbTypes, db_path: Path, **kwargs) -> bool:
  match db_type:
    case DbTypes.KP:
      key: Path = kwargs["key"]
      token: Path = kwargs["token"]
      with open_tk_store(db_type, db_path, key=key, token=token) as kp_db:
        return len(kp_db.entries) >= 0


# TODO: Remove
def save_dataframe(df: DataFrame, db_type: DbTypes, db_path: Path, **kwargs):
  match db_type:
    case DbTypes.KP:
      key: Path = kwargs["key"]
      token: Path = kwargs["token"]
      with open_tk_store(db_type, db_path, key=key, token=token) as kp_db:
        # TODO: dataclass for each db entry
        # TODO: delete, find existing then save if new
        # TODO: symmetric difference on uuid
        for _idx, row in df.iterrows():
          # entry: Entry = kp_db.find_entries(recursive=True, uuid=row["UUID"])
          entry: Entry = next(entry for entry in kp_db.entries if entry is not None and entry.title == row["Title"])
          if entry is None:
            kp_db.add_entry(
              destination_group=kp_db.root_group,
              url=row["URL"],
              title=row["Title"],
              username=row["UserName"],
              password=row["Password"],
            )
          else:
            # TODO: update
            pass
        kp_db.save()
    case _:
      raise TypeError("Unknown db type")
