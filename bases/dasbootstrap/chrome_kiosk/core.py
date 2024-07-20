"""Chrome kiosk script to launch a browser pointed at a given url."""

from __future__ import annotations

import os
import sys
import time

from playwright.sync_api import sync_playwright
from pynput import keyboard
from undetected_playwright import Tarnished


def _validate_data(user_data_dir: str) -> str:
  if not os.path.isdir(user_data_dir):
    raise ValueError(f"Invalid user data directory: {user_data_dir}")

  return user_data_dir


def _refresh_browser(page):
  print("Refreshing browser...")
  page.reload()


class ChromeKiosk:
  """ChromeKiosk.

  ChromeKiosk takes a url and a directory string to store the user profile.  It will then
  launch to the url with all test features disabled, in kiosk mode, refreshing the page periodically.

  Press CTRL+SHIFT+X to exit
  """

  def __init__(self, url: str, user_data_dir: str):
    """Initalize ChromeKiosk."""
    os.environ["PWDEBUG"] = ""
    os.makedirs(user_data_dir, exist_ok=True)

    self.url = url
    self.expanded_user_data_dir = _validate_data(os.path.expanduser(user_data_dir))

  def main(self):
    """Main function loop to be activated after initialization."""
    with sync_playwright() as p:
      browser = p.chromium.launch_persistent_context(
        headless=False,
        downloads_path=os.getcwd(),
        ignore_default_args=["--enable-automation"],
        args=[
          "--disable-dev-shm-usage",
          "--disable-blink-features=AutomationControlled",
          "--disable-infobars",
          "--start-maximized",
          "--no-sandbox",
          "--kiosk",
        ],
        locale="en_US.UTF-8",
        devtools=False,
        no_viewport=True,
        user_data_dir=self.expanded_user_data_dir,
      )

      Tarnished.apply_stealth(context=browser)
      page = browser.new_page()
      page.goto(self.url)

      def handle_exit():
        print("Exiting...")
        browser.close()
        sys.exit(0)

      def for_canonical(f):
        return lambda k: f(keyboard_listener.canonical(k))

      hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<shift>+x"), handle_exit)

      refresh_interval = 60 * 60 * 24
      last_refresh_time = time.time()

      while True:
        try:
          with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release),
          ) as keyboard_listener:
            keyboard_listener.join()

          page.wait_for_timeout(1000)

          current_time = time.time()
          if current_time - last_refresh_time >= refresh_interval:
            _refresh_browser(page)
            last_refresh_time = current_time

        except KeyboardInterrupt:
          break

      print("Exiting...")
