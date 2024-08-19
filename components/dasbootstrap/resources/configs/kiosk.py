from pydantic import AnyUrl
from simple_toml_settings import TOMLSettings


class ChromeKiosk(TOMLSettings):
  urls: list[AnyUrl]
  refresh: int
  page_timeout: int
  locale: str = "en_US.UTF-8"
  exit_key_pattern: str = "<ctrl>+<shift>+x"
