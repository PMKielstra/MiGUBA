from Benny.benny import Actor
from BibleAPI import BibleAPI
import requests
from html.parser import HTMLParser

class VerseHTMLParser(HTMLParser):

    paragraphs = []
    verses = []
    verse = ""
    parsing_verse_number = False

    def __init__(self, chapter, verse_number):
        HTMLParser.__init__(self)
        self.chapter = chapter
        self.verse_number = verse_number

    def new_verse(self):
        if self.verse != "":
            self.verses += [(self.chapter, self.verse_number, self.verse)]
            self.verse = ""
            self.verse_number += 1

    def new_paragraph(self):
        self.new_verse()
        if self.verses != []:
            self.paragraphs += [self.verses]
            self.verses = []
    
    def handle_starttag(self, tag, attrs):
        if tag == "span" and 'data-number' in dict(attrs):
            self.new_verse()
            self.parsing_verse_number = True
    
    def handle_endtag(self, tag):
        if self.parsing_verse_number and tag == "span":
            self.parsing_verse_number = False
        elif tag == "p":
            self.new_paragraph()
    
    def handle_data(self, data):
        if self.parsing_verse_number:
            self.verse_number = int(data)
            if self.verse_number == 1:
                self.chapter += 1
        else:
            self.verse = self.verse + data
    
    def result(self):
        return self.paragraphs

APIBIBLE_MAIN_URL = 'https://api.scripture.api.bible/v1'

class APIBible(BibleAPI, Actor):

    def APIBibleRequest(self, endpoint, params={}):
        response = requests.get(APIBIBLE_MAIN_URL + endpoint, params=params, headers={"api-key": self.api_key})
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
        copyright = rawResult['copyright']
        parser = VerseHTMLParser(int(verse_range['start_chapter']), int(verse_range['start_verse']))
        parser.feed(rawResult['content'])
        return parser.result(), copyright

    def get_verses(self, verse_ranges):
        return list(map(self.get_verse_range, verse_ranges))
