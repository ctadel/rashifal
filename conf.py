from enum import Enum
from pydantic import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.env')

load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PRODUCTION = True
    CHROME_BINARY = '/opt/google/chrome/webdriver'

    DEFAULT_LANGUAGE = 'hi'

    NLP_TRANSLATION_ENDPOINT = 'https://nlp-translation.p.rapidapi.com/v1/translate'
    NLP_TRANSLATION_API_SECRETS = {
                "X-RapidAPI-Key" : os.environ.get("X-RapidAPI-Key"),
                "X-RapidAPI-Host" : os.environ.get("X-RapidAPI-Host")
            }

settings = Settings()

class LANGUAGES(Enum):
    ne = 'NEPALI'
    en = 'ENGLISH'
    hi = 'HINDI'
