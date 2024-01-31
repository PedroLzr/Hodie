import requests
from bs4 import BeautifulSoup
from models.culture.word import *

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'})
DLE_URL = 'https://dle.rae.es'
IEDRA_URL = 'https://iedra.es'

def get_word_from_dle():
    try:

        print(">> Leyendo palabra del día en DLE")

        page = requests.get(DLE_URL, headers=HEADERS)
        page.close()

        dleSoup = BeautifulSoup(page.content, 'lxml')

        wordOfDay = dleSoup.find(id="wotd")
        word = wordOfDay.find("a").text.split(",")[0]
        word = ''.join([caracter for caracter in word if not caracter.isdigit()])

        wordUrl = DLE_URL + '/' + word
        wordPage = requests.get(wordUrl, headers=HEADERS)
        wordPage.close()

        wordSoup = BeautifulSoup(wordPage.content, 'lxml')

        result = wordSoup.find(id="resultados")
        article = result.article
        def_word_array = article.find_all('p', {'class': 'j'})

        definitions = []
        for p in def_word_array:

            # Eliminar todos los abbr (Abreviaturas)
            [abbr.decompose() for abbr in p.find_all('abbr')]
            # Eliminar spans con la clase 'h' que es la de los ejemplos
            [span.decompose() for span in p.find_all('span', recursive=False) if 'h' in span.get('class', [])]

            definitions.append(p.text)

        return Word(word, definitions, DLE_URL)

    except:
        print('Error buscando la palabra del DLE-RAE')
        return Word("Palabra no encontrada", "Palabra no encontrada", DLE_URL)

def get_word_from_iedra():
    try:

        print(">> Leyendo palabra del día en Iedra")

        page = requests.get(IEDRA_URL, headers=HEADERS)
        page.close()

        dleSoup = BeautifulSoup(page.content, 'lxml')

        wordOfDay = dleSoup.find(id="daily_word")
        word = wordOfDay.find("a").text

        wordUrl = DLE_URL + '/' + word
        wordPage = requests.get(wordUrl, headers=HEADERS)
        wordPage.close()

        wordSoup = BeautifulSoup(wordPage.content, 'lxml')

        result = wordSoup.find(id="resultados")
        article = result.article
        def_word_array = article.find_all('p', {'class': 'j'})

        definitions = []
        for p in def_word_array:

            # Eliminar todos los abbr (Abreviaturas)
            [abbr.decompose() for abbr in p.find_all('abbr')]
            # Eliminar spans con la clase 'h' que es la de los ejemplos
            [span.decompose() for span in p.find_all('span', recursive=False) if 'h' in span.get('class', [])]

            definitions.append(p.text)

        return Word(word, definitions, IEDRA_URL)

    except:
        print('Error buscando la palabra en Iedra')
        return Word("Palabra no encontrada", "Palabra no encontrada", IEDRA_URL)
