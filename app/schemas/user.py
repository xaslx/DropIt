from pydantic import BaseModel, ConfigDict



class UserIn(BaseModel):
    cookie_uuid: str


class UserOut(UserIn):
    id: int
    cookie_uuid: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

