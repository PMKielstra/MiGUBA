# MiGUBA
Michael's Grand Unified Bible API

A Benny-based API for accessing Bible verses.

```python
verse_references = [
    {
        'book': 'GEN',
        'start_chapter': '3',
        'start_verse': '1',
        'end_chapter': '3',
        'end_verse': '24'
    }
]

bible = Benny(BibleAPI)
bible.register(APIBible('<bible.api secret>'))
bible.register(ESVBible('<ESV API secret>'))

bible.get_verses('engKJV', verse_references)
bible.get_verses('ESV', verse_references)
```

The `get_verses` function returns two items: `text` and `copyright`.  The latter is a list of strings, each representing a paragraph in the Bible's required copyright statement.  The former is a list of tuples of the form `(chapter_number, verse_number, verse_text)`.  Chapter breaks are not marked.