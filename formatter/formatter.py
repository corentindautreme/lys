from abc import ABC, abstractmethod

class Formatter(ABC):
    @abstractmethod
    def format_post(self, post, events):
        pass