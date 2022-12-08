from html.parser import HTMLParser

IGNORE_CLASSES = ['extra_text', 'copyright']

class VerseHTMLParser(HTMLParser):

    paragraphs = []
    verses = []
    verse = ""
    parsing_verse_number = False
    ignoring = ""

    def __init__(self, number_tag, number_predicate, chapter, verse_number):
        HTMLParser.__init__(self)
        self.chapter = chapter
        self.verse_number = verse_number
        self.number_tag = number_tag
        self.number_predicate = number_predicate

    def new_verse(self):
        if self.verse.strip() != "":
            self.verses += [(self.chapter, self.verse_number, self.verse)]
            self.verse = ""
            self.verse_number += 1

    def new_paragraph(self):
        self.new_verse()
        if self.verses != []:
            self.paragraphs += [self.verses]
            self.verses = []

    def should_ignore(self, attrs):
        for iclass in IGNORE_CLASSES:
            if ('class', iclass) in attrs:
                return True
        return False
    
    def handle_starttag(self, tag, attrs):
        if tag == self.number_tag and self.number_predicate(attrs):
            self.new_verse()
            self.parsing_verse_number = True
        elif self.ignoring == "" and self.should_ignore(attrs):
            self.ignoring = tag
    
    def handle_endtag(self, tag):
        if tag == self.ignoring:
            self.ignoring = ""
        elif self.parsing_verse_number and tag == self.number_tag:
            self.parsing_verse_number = False
        elif tag == "p":
            self.new_paragraph()
    
    def handle_data(self, data):
        if self.ignoring != "":
            return
        if self.parsing_verse_number:
            self.verse_number = int(data)
            if self.verse_number == 1:
                self.chapter += 1
        else:
            self.verse = self.verse + data
    
    def result(self):
        return self.paragraphs