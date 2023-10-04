
import config_app
import os

app = config_app.button_prompts()


def test_app_file_storage() -> None:
    app.store_in_file()
    assert os.path.isfile("checks.txt")
