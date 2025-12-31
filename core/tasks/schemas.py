from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime



class TaskBaseSchema(BaseModel):
    title : str = Field(...,max_length=200,min_length=2,description="Title of the tasks")
    description : Optional[str] = Field(None,max_length=500,description="Description of the tasks")
    is_complete : bool = Field(...,description="State of the tasks")

class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id : int = Field(...,description="Unique identifier of the object")

    create_date : datetime = Field(...,description="Create date and time of the object")
    update_date : datetime = Field(...,description="Update date and time of the object")
