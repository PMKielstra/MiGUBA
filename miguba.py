from Benny.benny import Benny
from BibleAPI import BibleAPI
from APIBible import APIBible
import secretkeys

bible = Benny(BibleAPI)
bible.register(APIBible(secretkeys.APIBibleKey))
verses = [{'book': 'EXO', 'start_chapter': '18', 'start_verse': '2', 'end_chapter': '19', 'end_verse': '5'}]
print(bible.get_verses('engKJV', verses))
