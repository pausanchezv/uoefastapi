import os
from functools import lru_cache
from os import path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Base Settings """

    app_name: str = "Use of English Pro"
    admin_email: str = ""
    database_url: str = ""

    backend_cors_origins: str = ""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Database unit tests
    database_url_test: str = "sqlite:///./useofenglish_test.db"
    use_testing_database: bool = False

    oauth2_secret_key: str = ""
    oauth2_algorithm: str = ""
    oauth2_access_token_expire_minutes: int = 60 * 24 * 365

    class Config:
        """
        Allows the app to pick up the values from the .env file
        """
        env_file = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/.env"
        env_file_encoding = 'utf-8'

    @property
    def logs_dir(self):
        """
        Directory where the logs are. It gets created if it does not exist
        """

        logs_dir: str = f'{self.base_dir}/logs'

        if not (path.exists(logs_dir) and path.isdir(logs_dir)):
            os.mkdir(logs_dir)

        return logs_dir

    def activate_testing_database(self):
        """
        Changes to the testing database
        """
        self.use_testing_database = True


@lru_cache()
def get_settings():
    return Settings()




