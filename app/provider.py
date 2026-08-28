# PromptGate Provider Module

from typing import Dict, Optional


class Provider:
    """Base provider class for generating outputs from prompts."""

    def generate(self, prompt: str) -> str:
        """Generate an output from the given prompt.

        Args:
            prompt: The input prompt to generate an output for.

        Returns:
            The generated output.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class MockProvider(Provider):
    """A mock provider that returns predefined outputs or 'MOCK' by default."""

    def __init__(self):
        self.prompt_output_map: Dict[str, str] = {}

    def generate(self, prompt: str) -> str:
        """Generate a mock output for the given prompt.

        Args:
            prompt: The input prompt.

        Returns:
            The mapped output if prompt exists in the map, otherwise 'MOCK'.
        """
        return self.prompt_output_map.get(prompt, "MOCK")