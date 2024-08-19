from __future__ import annotations

import os
import tarfile
import tempfile
import zipfile
from enum import StrEnum, auto
from io import BytesIO
from pathlib import Path

import zstandard as zstd

ALLOWED_MEMBERS = [f"{Path.home()}"]


def _pathify(*pathlike: str | Path) -> list[Path]:
  return [Path(path) for path in pathlike]


class CompressionTypes(StrEnum):
  ZIP = auto()
  ZSTD = auto()


def pack(
  src_dir: Path,
  out_file: Path | str,
  compression_type: CompressionTypes = CompressionTypes.ZSTD,
):
  """Use tar to create an archive and then a designated compression format to compress the archive.

  Args:
    src_dir: The path to the folder to compress.
    out_file: The path to the target archive file.
    compression_type: The type of compression to use
  """
  src_dir_pth, out_file_pth = _pathify(src_dir, out_file)

  with tarfile.open(f"{src_dir_pth}.tar", "x") as tar_file:
    tar_file.add(src_dir_pth, arcname=src_dir_pth)

  match compression_type:
    case CompressionTypes.ZSTD:
      cctx = zstd.ZstdCompressor(level=3, write_checksum=True, write_content_size=True, threads=-1)
      with open(f"{src_dir_pth}.tar", "rb") as tar_file, open(out_file_pth, "xb") as zstd_file:
        zstd_file.write(cctx.compress(tar_file.read()))
      os.remove(f"{src_dir_pth}.tar")
    case CompressionTypes.ZIP:
      raise NotImplementedError
    case _:
      raise TypeError(f"{compression_type} is not implemented")


def unpack(
  in_file: Path | str,
  out_dir: Path | str,
  compression_type: CompressionTypes = CompressionTypes.ZSTD,
):
  """:param out_dir:
  :param in_file:
  :param compression_type:
  :return:
  """
  in_file_pth, out_dir_pth = _pathify(in_file, out_dir)

  match compression_type:
    case CompressionTypes.ZSTD:
      temp_in_stream: bytes = in_file_pth.read_bytes()
      dctx = zstd.ZstdDecompressor()
      temp_out_stream: BytesIO = BytesIO(dctx.decompress(data=temp_in_stream))

      # assume tar output, but verify
      if not tarfile.is_tarfile(temp_out_stream):
        raise OSError("This array of bytes does not seem to be a tarfile")

      if not out_dir_pth.exists():
        out_dir_pth.mkdir(parents=True, exist_ok=True)

      with tarfile.open(mode="r", fileobj=temp_out_stream) as tar_file:
        members_to_extract = [m for m in tar_file.getmembers() if m.name in ALLOWED_MEMBERS]
        tar_file.extractall(members=members_to_extract, path=out_dir_pth)
    case _:
      raise TypeError(f"{compression_type} is not implemented")


def zip_files(*files: Path) -> Path:
  with (
    tempfile.NamedTemporaryFile(delete=False, delete_on_close=False) as temp_file,
    zipfile.ZipFile(temp_file.name, mode="w") as zip_file,
  ):
    for file in files:
      zip_file.write(file)

    return Path(temp_file.name)


def ensure_path(*files: Path) -> bool:
  all_exist: bool = True
  for _, path in enumerate([path for path in files if not path.exists()]):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.is_file()
    if all_exist:
      all_exist = False
  return all_exist


def backup_and_generate(*files):
  pass


def delete_files(*files: Path):
  for file in files:
    file.unlink(missing_ok=True)
