from abc import ABC, abstractmethod
from unidecode import unidecode


class BaseComponent(ABC):

    def run(self):
        self.extraction()
        self.transformation()
        self.load()

    @abstractmethod
    def extraction(self) -> None:
        pass

    @abstractmethod
    def transformation(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

    # Normalizar las cadenas de texto
    def normalize_text(self, text):
        return unidecode(text).upper().strip()
