from pydantic import BaseModel, Field


class BugReport(BaseModel):
    title: str
    steps: list[str]
    questions: list[str]
    expected: str | None = Field(default=None)
    actual: str | None = Field(default=None)