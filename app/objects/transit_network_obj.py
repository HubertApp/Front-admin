from pydantic import BaseModel, Field


class TransitNetworkResponseObj (BaseModel):
    id:int
    title:str
    description:str
    type:str
    api_key:str = Field(validation_alias="apiKey")
    endpoint_url:str = Field(validation_alias="endpointUrl")
