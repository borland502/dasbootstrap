"""
PS: all password entries are in cleartext between server and browser, DO NOT DEPLOY THIS ON A SERVER. EVER.
https://gist.github.com/andfanilo/4bd880ea760d67d5afc40d215ef060e1
"""

import logging
from io import BytesIO, StringIO
from pathlib import Path

import pandas as pd
import streamlit as st
from pandas import DataFrame
from pykeepass.pykeepass import CredentialsError, PyKeePass, create_database
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_extras.row import row
from xdg_base_dirs import xdg_config_home, xdg_data_home, xdg_state_home

from dasbootstrap.files import delete_files, ensure_path, zip_files
from dasbootstrap.keegen.core import gen_passphrase, gen_utf8
from dasbootstrap.trapper_keeper.tk import save_dataframe, DbTypes, validate_tk_store

ENTRY_XPATH: str = "//Entry[UUID != ''][String[Key='Title' or Key='Password' or Key='UserName' or Key='URL']]"

log = logging.getLogger("automation_station")

keys: list[str] = ["Title", "UserName", "Password", "URL"]
token_path: Path = xdg_config_home().joinpath(st.secrets["files"]["token"])
key_path: Path = xdg_state_home().joinpath(st.secrets["files"]["key"])
db_path: Path = xdg_data_home().joinpath(st.secrets["files"]["db"])

paths: list[Path] = [token_path, key_path, db_path]
DOWNLOAD_FILE_NAME: str = "download_file.zip"


@st.cache_data
def _process_file(file: UploadedFile, dest: Path, to_utf: bool = False):
  log.info(f"processing {UploadedFile}")
  if to_utf:
    file_txt = StringIO(file.getvalue().decode("utf-8"))
    with open(dest, encoding="utf-8", mode="w") as file_out:
      file_out.write(file_txt.getvalue())
  else:
    file_bin = BytesIO(file.getvalue())
    with open(dest, mode="w+b") as file_out:
      file_out.write(file_bin.read())


def _process_data_table():
  kp_db = PyKeePass(
    filename=db_path,
    keyfile=key_path,
    password=token_path.read_text(encoding="utf-8"),
  )
  with st.form(key="df_form"):
    df: DataFrame = st.data_editor(
      # TODO: Bug if the database is empty no columns will display
      _to_dataframe(kp_db),
      use_container_width=True,
      height=720,
      hide_index=True,
      column_order=keys,
      num_rows="dynamic",
    )
    st.divider()
    st.form_submit_button(
      label="Submit",
      on_click=save_dataframe,
      args=[df.copy(deep=True), DbTypes.KP],
      kwargs={"db_path": db_path, "key": key_path, "token": token_path},
    )


# TODO: void cache if db updated
def _download_action() -> BytesIO:
  pass


# TODO: Migrate paths to home page as db will be needed for other pages
def _save_paths_to_session(*args: Path):
  """Saves paths to the Streamlit session state if they are not already present."""
  for path in args:
    if path.name not in st.session_state:
      st.session_state[path.name] = path


# TODO: Pass in elements to extract
@st.cache_data
def _to_dataframe(_kp_db: PyKeePass) -> DataFrame:
  """Create a simplified DataFrame from a KeePass XML string

  :param _kp_db: raw xml data from pykeepass as etree (e.g. kb_dp.xml())
  :return: DataFrame containing Title, Username, Password, and URL
  """
  root = _kp_db.tree

  # Extract data using XPath
  entries = root.findall(".//Entry")
  data = []
  for entry in entries:
    entry_data = {}
    uuid: str = entry.find("UUID").text
    entry_data["UUID"] = uuid
    for string_element in entry.findall("String"):
      key = string_element.find("Key").text
      if key is not None and key in keys:
        value = string_element.find("Value").text
        entry_data[key] = value
    data.append(entry_data)

  # Create DataFrame
  return pd.DataFrame(data)


def _create_sample_entries(kp_db: PyKeePass):
  for entry in st.secrets["entries"]:
    title: str = entry["title"]
    username: str = entry["username"]
    password: str = entry["password"]
    url: str = entry["url"]
    kp_db.add_entry(
      destination_group=kp_db.root_group,
      url=url,
      title=title,
      username=username,
      password=password,
    )
  kp_db.save()


def _create_sidebar_row(path: Path, found_row, create_row):
  match path.name:
    case token_path.name:
      if token_path.exists():
        found_row.markdown(f"#### :heavy_check_mark: {token_path.name}")
        if found_row.button(label="Delete", key="del_token"):
          delete_files(token_path)
          st.rerun()
      else:
        if create_row.button(label="Generate Token", key="gen_token"):
          token_path.write_text(
            encoding="utf-8", data=gen_passphrase()
          )
          st.rerun()
        kp_token = create_row.file_uploader(
          "Select keepass token", key="kp_token_upload"
        )
        if kp_token is not None:
          _process_file(kp_token, dest=token_path)
          st.rerun()
    case key_path.name:
      if key_path.exists():
        found_row.markdown(f"#### :heavy_check_mark: {key_path.name}")
        if found_row.button(label="Delete", key="del_key"):
          delete_files(key_path)
          st.rerun()
      else:
        if create_row.button(label="Generate Key", key="gen_key"):
          key_path.write_text(encoding="utf-8", data=gen_utf8())
          st.rerun()
        kp_key = create_row.file_uploader(
          "Select keepass key", key="kp_key_upload"
        )
        if kp_key is not None:
          _process_file(kp_key, dest=key_path)
          st.rerun()
    case db_path.name:
      if db_path.exists():
        found_row.markdown(f"#### :heavy_check_mark: {db_path.name}")
        if found_row.button(label="Delete", key="del_db"):
          delete_files(db_path)
          st.cache_data.clear()
          st.rerun()
      else:
        if create_row.button(label="Generate Database", key="gen_db"):
          # TODO: Check for key and token
          kp_db: PyKeePass = create_database(
            filename=db_path,
            keyfile=key_path,
            password=token_path.read_text(encoding="utf-8"),
          )
          # With no entries the datatable will have no columns, so generate a sample
          _create_sample_entries(kp_db)
          st.rerun()
        kp_db_bin = create_row.file_uploader(
          "Select keepass db", key="kp_db_upload"
        )
        if kp_db_bin is not None:
          _process_file(kp_db_bin, dest=db_path)
          st.rerun()
    case _:
      st.warning(f"Unknown {path}")


@st.cache_data
def _create_download():
  return zip_files(db_path, key_path, token_path)


def main():
  logging.basicConfig(filename="automation_station.log", level=logging.INFO)
  st.title("Keepass browser")
  all_exist = ensure_path(db_path, key_path, token_path)
  with st.sidebar:
    found_row = row([0.75, 0.25], gap="small", vertical_align="center")
    create_row = row(1, gap="small", vertical_align="center")
    for path in paths:
      _create_sidebar_row(path, found_row, create_row)

  if all_exist:
    try:
      validate_tk_store(
        DbTypes.KP, db_path, token=token_path, key=key_path
      )
      _process_data_table()
    except CredentialsError:
      st.error("""
        ## Invalid credentials

        Either upload the correct token, key, & db or restart from scratch
        """)
    download_file: Path = _create_download()
    if download_file is None:
      raise FileNotFoundError
    else:
      st.download_button(
        key="download_button",
        disabled=(not all_exist),
        label="Download Button",
        file_name=DOWNLOAD_FILE_NAME,
        mime="application/zip",
        data=download_file.read_bytes(),
      )


if __name__ == "__main__":
  st.set_page_config(
    page_title="Streamlit Keepass Browser",
    page_icon=":lock:",
    layout="wide",
  )
  main()
