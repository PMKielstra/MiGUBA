from Benny.benny import SingleKeyActor
from BibleAPI import BibleAPI
import requests
import re
from VerseHTMLParser import VerseHTMLParser
from html import unescape

ESV_MAIN_URL = 'https://api.esv.org/v3/passage'

COPYRIGHT_EXTRACTION_REGEX = """<p class=\\\"copyright\\\">(.+?)</p>"""

class ESVBible(BibleAPI, SingleKeyActor):

    def ESVBibleRequest(self, endpoint, params={}):
        response = requests.get(ESV_MAIN_URL + endpoint, params=params, headers={"Authorization": f"Token {self.api_key}"})
        assert(response.status_code == 200) # OK
        return response.json()

    def __init__(self, api_key):
        self.api_key = api_key

    def register_key(self):
        return 'ESV'

    def clean(self, string):
        return unescape(string).replace('\xa0', ' ')

    def parse_result(self, verse_range, result):
        parser = VerseHTMLParser('b', lambda attrs: ('class', 'verse-num') in attrs or ('class', 'verse-num inline') in attrs, int(verse_range['start_chapter']), int(verse_range['start_verse']))
        parser.feed(result)
        return parser.result()

    def get_verses(self, verse_ranges):
        references = [f"""{verse_range['book']}.{verse_range['start_chapter']}.{verse_range['start_verse']}-{verse_range['end_chapter']}.{verse_range['end_verse']}""" for verse_range in verse_ranges]
        full_ref_string = ";".join(references)
        raw_results = self.ESVBibleRequest(f'/html', {
            'q': full_ref_string,
            'include-copyright': 'true',
            'include-short-copyright': 'false',
            'include-footnotes': 'false',
            'include-headings': 'false',
            'include-chapter-numbers': 'false'
        })
        copyright = re.findall(COPYRIGHT_EXTRACTION_REGEX, self.clean(raw_results['passages'][0]))
        return [self.parse_result(verse_range, self.clean(result)) for verse_range, result in zip(verse_ranges, raw_results['passages'])], copyright
        
