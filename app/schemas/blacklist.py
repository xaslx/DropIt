from pydantic import BaseModel, Field, ConfigDict




class BlackList(BaseModel):
    ip_address: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

