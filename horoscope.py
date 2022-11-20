from datetime import datetime
from conf import settings
import requests
from bs4 import BeautifulSoup as Soup
import re

RASHIS = [
        ("aries","mesh","mess","mace"),
        ("taurus","vrish","vrishabh","bris"),
        ("gemini","mithun"),
        ("cancer","kark"),
        ("leo","sinh","singh"),
        ("virgo","kanya"),
        ("libra","tula","tulaa"),
        ("scorpio","vrishchak"),
        ("sagittarius","dhanu","dhanus"),
        ("capricorn","makar"),
        ("aquarius","kumbh"),
        ("pisces","mean","meen")
    ]

class HoroscopeKeeper:

    def __init__(self, language):

        self.today = datetime.today().date()
        self.cached = False
        self.data = {}
        self.language = language

        HoroscopeKeeper.LOCALITY[language] = self

    LOCALITY = {}

    def __repr__(self):
        return f'<HoroscopeKeeper: "{self.language}">'

    def __str__(self):
        return f'[Language: {self.language}, Cached: {self.cached}, Date: {self.today}]'

    def __new__(cls, *args, **kwargs):

        if HoroscopeKeeper.LOCALITY.get(args[0]):
            return cls.LOCALITY.get(args[0])

        return super().__new__(cls)


class RashiFetch:

    def __init__(self, language):

        self.language = language

        self.RASHI_MAPPER = {}
        for number, rashi in enumerate(RASHIS):
            for name in rashi:
                self.RASHI_MAPPER[name] = number + 1


    def get_horoscope_numer(self, rashi):
        return self.RASHI_MAPPER.get(rashi)

    def get_english_name(self, rashi):
        number = self.get_horoscope_numer(rashi)
        if number:
            return RASHIS[number-1][0]

    @staticmethod
    def get_rashi_in_hindi():

        document = Soup(requests.get('https://hindi.webdunia.com/astrology-daily-horoscope').content, 'html.parser')
        rashis = document.find_all('div', class_='zdc_daily')

        RASHIFALL = {}
        for index, (horoscope, *_) in enumerate(RASHIS):
            text = re.sub(r'।\t.*\n.*','।', re.sub(r'\n\n\n.*\r\n\t\t\t\t\t','', rashis[index].text)).strip()
            RASHIFALL[horoscope] = text

        return RASHIFALL

    def translate(self, data: dict, from_language = 'np'):

        querystring = {
                "protected_words":'$',
                "to" : self.language,
                "from" : from_language
            }

        headers = settings.NLP_TRANSLATION_API_SECRETS

        response_data = {}
        for horoscope,rashifall in data.items():
            querystring['text'] = rashifall
            response = requests.request(
                    "GET",
                    settings.NLP_TRANSLATION_ENDPOINT,
                    headers=headers,
                    params=querystring
                )
            response_data[horoscope] = response.json().get('translated_text').get(self.language)

        return response_data



        #RESPONSE = ''

        #for i in range(0,12,2):
        #    querystring['text'] = ''
        #    for j in range(2):
        #        querystring['text'] += data[list(data.keys())[i+j]] + '$'

        #    response = requests.request(
        #            "GET",
        #            settings.NLP_TRANSLATION_ENDPOINT,
        #            headers=headers,
        #            params=querystring
        #        )
        #    print(response.json().get('translated_text').get(self.language),"\n")

        #    RESPONSE += response.json().get('translated_text').get(self.language) + '$'

        #print("*"*100,RESPONSE)
        #response_data = dict(zip(data.keys(),RESPONSE.split('$')))
        #return response_data
