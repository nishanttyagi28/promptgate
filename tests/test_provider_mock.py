import pytest
from app.providers.mock import MockProvider


def test_mock_provider_default_output():
    """Test that the mock provider returns 'MOCK' by default."""
    provider = MockProvider()
    result = provider.generate("any prompt")
    assert result == "MOCK"


def test_mock_provider_custom_output():
    """Test that the mock provider returns custom outputs when configured."""
    provider = MockProvider()
    provider.prompt_output_map = {
        "prompt1": "output1",
        "prompt2": "output2"
    }
    
    assert provider.generate("prompt1") == "output1"
    assert provider.generate("prompt2") == "output2"
    assert provider.generate("prompt3") == "MOCK"


def test_mock_provider_empty_prompt():
    """Test that the mock provider handles empty prompts."""
    provider = MockProvider()
    result = provider.generate("")
    assert result == "MOCK"