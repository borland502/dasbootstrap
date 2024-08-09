from __future__ import annotations

import os
from collections.abc import Sequence
from contextlib import AbstractContextManager
from io import StringIO
from pathlib import Path

from pykeepass import PyKeePass, create_database


def _create_kp_db(kp_fp: Path, kp_token: Path, kp_key: Path | None = None) -> PyKeePass:
  """Create a new keepass vault in the KEEPASS_DB_PATH, with the KEEPASS_DB_KEY, and KEEPASS_DB_TOKEN."""
  if not kp_fp.is_file():
    # make the directory at least if the database does not exist
    kp_fp.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
  # Token and key must exist in the target destinations ahead of time
  if not kp_token.is_file():
    # make the directory at least if the database does not exist
    kp_token.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    raise FileNotFoundError(f"Token file not found in path {kp_token}")
  if kp_key is not None and not kp_key.is_file():
    # make the directory at least if the database does not exist
    kp_key.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    raise FileNotFoundError(f"Key file not found in path {kp_key}")
  return create_database(
    kp_fp,
    password=kp_token.read_text("utf-8").strip("\n"),
    keyfile=kp_key,
  )


REF_PREFIX = "ref@"
REF_SEP = "/"
REF_SEP2 = ":"
ATTR_TITLE = "__title__"
ATTR_USERNAME = "__username__"
ATTR_PASSWORD = "__password__"
ATTR_URL = "__url__"


def _validate_ref(ref: str) -> None:
  if not ref:
    raise ValueError("Empty ref")
  if not ref.startswith(REF_PREFIX):
    raise ValueError(f"Invalid ref: {ref}, prefix {REF_PREFIX!r} expected")
  if ref.removeprefix(REF_PREFIX).count(REF_SEP) < 1:
    raise ValueError(
      f"Invalid ref: {ref}, at least 1 separator {REF_SEP!r} expected",
    )
  if ref.removeprefix(REF_PREFIX).count(REF_SEP2) != 1:
    raise ValueError(
      f"Invalid ref: {ref}, exactly 1 separator {REF_SEP2!r} expected",
    )


def _parse_ref(ref: str) -> tuple[list[str], str]:
  _validate_ref(ref)
  ref = ref.removeprefix(REF_PREFIX)
  _path, attribute = ref.rsplit(REF_SEP2, maxsplit=1)
  path = _path.split(REF_SEP)
  return path, attribute


class KeepassStore(PyKeePass):
  def __init__(self, kp_fp: Path, kp_token: Path, kp_key: Path | None = None):
    super().__init__(
      filename=kp_fp,
      password=kp_token.read_text(encoding="utf-8"),
      keyfile=kp_key,
    )

  def __enter__(self) -> AbstractContextManager:
    return self

  def load_ref(self, ref: str) -> str:
    path, attribute = _parse_ref(ref)
    entry = self.find_entries(path=path)
    if entry is None:
      raise KeyError(f"Entry {path!r} not found")
    if attribute == ATTR_TITLE:
      out: str = entry.title
    elif attribute == ATTR_USERNAME:
      out = entry.username
    elif attribute == ATTR_PASSWORD:
      out = entry.password
    elif attribute == ATTR_URL:
      out = entry.url
    else:
      out = entry.custom_properties[attribute]
    if out.startswith(REF_PREFIX):
      if attribute == ATTR_TITLE:
        raise ValueError(f"Invalid ref: {ref}, title cannot be a ref")
      return self.load_ref(out)
    return out

  def load_env(self, entry_path: Sequence[str]) -> None:
    env = self.env(entry_path=entry_path)
    for k, v in env.items():
      os.environ[k] = v

  def env(self, entry_path: Sequence[str]) -> dict[str, str]:
    """:param self:
    :param entry_path:
    :return:
    """
    entry = self.find_entries(path=entry_path)
    if entry is None:
      raise KeyError(f"Entry {entry_path!r} not found")
    kv = entry.custom_properties
    env = {}
    for k, v in kv.items():
      if v.startswith(REF_PREFIX):
        env[k] = self.load_ref(v)
      else:
        env[k] = v
    return env

  def write_env(
    self,
    entry_path: Sequence[str],
    env: dict[str, str],
    create_if_not_exists: bool = True,
  ) -> None:
    entry = self.find_entries(path=entry_path)
    if entry is None:
      if create_if_not_exists:
        raise NotImplementedError
      else:
        raise KeyError(f"Entry {entry_path!r} not found")
    for k, v in env.items():
      entry.set_custom_property(k, v)
    self.save()

  def dump_env(self, entry_path: Sequence[str], output_format: str) -> StringIO:
    with StringIO() as sink:
      for k, v in self.env(entry_path):
        match output_format:
          case "env":
            if output_format == "env":
              sink.write(f"{k}={v}")
            elif output_format == "docker":
              sink.write(f"-e {k}={v}")
            elif output_format == "shell":
              sink.write(f"export {k}={v}")
            else:
              raise ValueError(f"Invalid format: {output_format!r}")
      return sink

  def __exit__(self, __exc_type, __exc_value, __traceback):
    super().__exit__(__exc_type, __exc_value, __traceback)
