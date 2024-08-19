from pathlib import Path

from sqlite_utils import Database


class SqliteStore(Database):
  def __init__(self, sp_fp: Path):
    super().__init__()

  def __enter__(self) -> Database:
    return self

  def __exit__(self, __exc_type, __exc_value, __traceback):
    self.close()
