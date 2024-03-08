from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

IP_ADDRESS = os.getenv("IP_ADDRESS")

print(IP_ADDRESS)

# from functools import lru_cache
#
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
#
#
# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
#     VERSION : str = 'Filili'
#     APP_NAME: str
#     DB_HOST : str
#     DB_NAME : str
#     DB_PASS : str
#     DB_PORT : str
#     DB_USER : str
#
#
# @lru_cache
# def get_settings() -> Settings:
#     settings = Settings()
#     return settings

