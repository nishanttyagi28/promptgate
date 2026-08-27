from pydantic import BaseModel

class PromptCase(BaseModel):
    id: str
    prompt: str
    expect_contains: str
