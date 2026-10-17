from pydantic import BaseModel

class Question(BaseModel):
    text: str

class Token(BaseModel):
    input_token: int
    output_token: int

class Answer(BaseModel):
    text: str
    token: Token
    cost: float
    confidence: float