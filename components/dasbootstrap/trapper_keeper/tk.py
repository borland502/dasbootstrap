"""
Trapper Keeper interface to various DB Stores noted by class DbTypes.
"""

import contextlib
from enum import StrEnum, auto
from pathlib import Path

from pandas import DataFrame
from pykeepass.entry import Entry

from dasbootstrap.trapper_keeper.stores.bolt_kvstore import BoltStore
from dasbootstrap.trapper_keeper.stores.keepass_store import KeepassStore


class DbTypes(StrEnum):
    BOLT: str = auto()
    KP: str = auto()
    SQLITE: str = auto()


def open_tk_store(
    db_type: DbTypes, db_path: Path, **kwargs
) -> contextlib.AbstractContextManager:
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

def validate_tk_store(db_type: DbTypes, db_path: Path, **kwargs) -> bool:
  match db_type:
    case DbTypes.KP:
      key: Path = kwargs["key"]
      token: Path = kwargs["token"]
      with open_tk_store(db_type, db_path, key=key, token=token) as kp_db:
        if len(kp_db.entries) >= 0:
          return True
        else:
          return False

def save_dataframe(
    df: DataFrame, db_type: DbTypes, db_path: Path, **kwargs
):
    match db_type:
        case DbTypes.KP:
            key: Path = kwargs["key"]
            token: Path = kwargs["token"]
            with open_tk_store(
                db_type, db_path, key=key, token=token
            ) as kp_db:
                # TODO: dataclass for each db entry
                # TODO: delete, find existing then save if new
                # TODO: symmetric difference on uuid
                for idx, row in df.iterrows():
                    # entry: Entry = kp_db.find_entries(recursive=True, uuid=row["UUID"])
                    entry: Entry = [entry for entry in kp_db.entries if entry is not None and entry.title == row["Title"]][0]
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
