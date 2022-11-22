from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from selenium.webdriver.support.ui import Select

from drivers import WebDriver
from conf import LANGUAGES, settings
from horoscope import RashiFetch, HoroscopeKeeper

from datetime import datetime

app = FastAPI()

locale = {language:HoroscopeKeeper(language) for language in LANGUAGES.__members__.keys()}
default = locale[settings.DEFAULT_LANGUAGE]

@app.get('/rashifall/{rashi}/')
def get_rashifall(rashi: str, language: str = 'hi'):

    if language not in LANGUAGES.__members__.keys():
        return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = dict(
                    status = 'FAIL',
                    message = f'Unsupported language: {language}'
                ),
            )

    try:
        manager = RashiFetch(language)
        session = locale[language]

    except Exception as e:
        return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = dict(
                    status = 'FAIL',
                    message = f'Exception: {str(e)}'
                ),
            )

    english_rashi = manager.get_english_name(rashi)

    if not english_rashi:
        return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = dict(
                    status = 'FAIL',
                    message = f'{rashi} rashi not found'
                ),
            )


    if default.today != datetime.today().date() or not default.cached:
        default.data = RashiFetch.get_rashi_in_hindi()
        default.cached = True
        default.today = datetime.today().date()


    if session.today != datetime.today().date() or not session.cached:
        session.data = manager.translate(default.data)
        session.cached = True
        session.today = datetime.today().date()

    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = dict(
                status = 'PASS',
                horoscope = english_rashi,
                message = session.data.get(english_rashi)
            ),
        )
