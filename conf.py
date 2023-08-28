from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
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
