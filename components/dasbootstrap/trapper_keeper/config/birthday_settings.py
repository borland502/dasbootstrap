from simple_toml_settings import TOMLSettings


class BirthdayReminder(TOMLSettings):
  """Settings for birthday reminder.

  Args:
      TOMLSettings (_type_): _description_
  """

  db_pth: str = ""
  refresh_period: int = 3600

  def __post_create_hook__():
    pass


settings: BirthdayReminder = BirthdayReminder("birthday_reminder", xdg_config=True, schema_version="1")

print(settings.get_settings_folder())
