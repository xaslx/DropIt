from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime




class FileSchema(BaseModel):
    filename: str
    url: str
    upload_date: datetime
    user_id: int
    content_type: str


class FileSchemaOut(FileSchema):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)