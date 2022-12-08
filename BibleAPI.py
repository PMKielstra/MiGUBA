from abc import ABC, abstractmethod

class BibleAPI(ABC):
    @abstractmethod
    def get_verses(self, verse_ranges):
        pass
