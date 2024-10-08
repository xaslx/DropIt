from pydantic import BaseModel, ConfigDict



class UserIn(BaseModel):
    ip_address: str


class UserOut(UserIn):
    id: int
    ip_address: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

