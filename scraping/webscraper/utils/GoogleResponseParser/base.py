# Abstract base class
from abc import ABC, abstractmethod


class GoogleSearchResponseParserBase(ABC):
    @abstractmethod
    def image_sources(self, response):
        pass
