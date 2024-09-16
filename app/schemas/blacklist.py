from pydantic import BaseModel, Field, ConfigDict




class BlackList(BaseModel):
    id: int
    ip_address: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

