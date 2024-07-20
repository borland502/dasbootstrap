"""BoltDB context manager module."""

from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path

from boltdb import BoltDB
from boltdb.tx import Tx


class BoltStore(AbstractContextManager):
  """Basic context manager for accessing BoltDB."""

  def __entry__(self) -> Tx:
    return self.tx

  def __init__(self, bp_fp: Path, readonly: bool):
    self.bolt_db = BoltDB(filename=bp_fp, readonly=readonly)
    self.tx = self.bolt_db.begin(writable=(not readonly))
    self.readonly = readonly
    self.bolt_db_methods = [item for item in dir(BoltDB) if not item.startswith("_")]
    self.tx_methods = [item for item in dir(Tx) if not item.startswith("_")]
    self.bp_fp = bp_fp

  def __getattr__(self, item):
    def method(*args):
      # boltdb lib calls close on del and that behavior is neither wanted nor desirable
      if item in self.bolt_db_methods:
        return getattr(self.bolt_db, item)(*args)
      if item in self.tx_methods:
        return getattr(self.tx, item)(*args)

      raise AttributeError

    return method

  def __exit__(self, __exc_type, __exc_value, __traceback):
    if not self.readonly:
      self.tx.write()
      self.tx.commit()

    self.tx.close()
