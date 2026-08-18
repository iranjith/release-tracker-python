from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

project_name_constraints = StringConstraints(
    strip_whitespace=True, min_length=2, max_length=120
)
StrippedName = Annotated[str, project_name_constraints]


class ProjectCreate(BaseModel):
    name: StrippedName
    description: str | None = Field(default=None, max_length=1000)
