from pydantic import BaseModel


class QuestionRequestPayload(BaseModel):
    type: str
    arithmetic: str
    digits: int
    numquestions: int


class QuestionResponseGeneric(BaseModel):
    questions: list[str]
    answers: list[int]
