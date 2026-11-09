from pydantic import BaseModel, Field, field_validator


class BagRequestSchema(BaseModel):
    text: str = Field(min_length=10, max_length=3000, description="Ошибка пользователя")

    @field_validator("text")
    def text_validator(cls, v):
        if not v:
            raise ValueError

        if not v.split():
            raise ValueError

        return v