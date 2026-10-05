from pydantic import BaseModel, Field 



class MajorsAdd(BaseModel):
    major_name: str = Field(description="name of the major")
    major_description: str = Field(description="Major description")
    count_students: int = Field(0, description="students count")



class MajorsUpdate(BaseModel):
    major_name: str | None = None
    major_description: str | None = None


class MajorsDelete(BaseModel):
    major_name: str | None = None
    major_description: str | None = None