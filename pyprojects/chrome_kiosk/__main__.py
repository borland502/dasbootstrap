"""Main module for chrome-kiosk."""

from chrome import ChromeKiosk
from typer import Typer

app = Typer()


@app.command(short_help="Launch a Chromium browser for an Application", no_args_is_help=True)
def goto_url(url: str, user_data_dir: str):
  """Launch the kiosk module and go to the given url with the given user profile directory."""
  kiosk = ChromeKiosk(url=url, user_data_dir=user_data_dir)
  kiosk.main()
