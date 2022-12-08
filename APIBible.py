from Benny.benny import Actor
from BibleAPI import BibleAPI
import requests
from VerseHTMLParser import VerseHTMLParser

APIBIBLE_MAIN_URL = 'https://api.scripture.api.bible/v1'

class APIBible(BibleAPI, Actor):

    def APIBibleRequest(self, endpoint, params={}):
        response = requests.get(APIBIBLE_MAIN_URL + endpoint, params=params, headers={"api-key": self.api_key})
        assert(response.status_code == 200) # OK
        return response.json()

    def __init__(self, api_key):
        self.api_key = api_key
        bibleList = self.APIBibleRequest('/bibles')['data']
        self.bibles = {b['abbreviation']:b['id'] for b in bibleList}

    def register_keys(self):
        return self.bibles.keys()

    def get_verse_range(self, verse_range):
        bible = self.bibles[self.get_current_key()]
        rawResult = self.APIBibleRequest(f"""/bibles/{bible}/passages/{verse_range['book']}.{verse_range['start_chapter']}.{verse_range['start_verse']}-{verse_range['book']}.{verse_range['end_chapter']}.{verse_range['end_verse']}""", params={"include-notes": "false"})['data']
        self.copyright = rawResult['copyright']
        parser = VerseHTMLParser('span', lambda attrs: 'data-number' in dict(attrs), int(verse_range['start_chapter']), int(verse_range['start_verse']))
        parser.feed(rawResult['content'])
        return parser.result()

    def get_verses(self, verse_ranges):
        return list(map(self.get_verse_range, verse_ranges)), [self.copyright]
