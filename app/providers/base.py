from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate output based on the given prompt."""
        pass