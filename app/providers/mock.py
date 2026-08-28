from .base import BaseProvider

class MockProvider(BaseProvider):
    def __init__(self):
        self.prompt_output_map = {}
        self.default_output = "MOCK"

    def generate(self, prompt: str) -> str:
        """Generate output based on the given prompt."""
        return self.prompt_output_map.get(prompt, self.default_output)