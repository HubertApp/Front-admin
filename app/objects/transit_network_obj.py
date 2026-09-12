from typing import List, Optional

from pydantic import BaseModel, Field


class ResourceResponseObj(BaseModel):
    title: str
    format: str
    endpointUrl: str


class TransitNetworkResponseObj(BaseModel):
    title: str = Field(validation_alias="name")
    external_id: str = Field(validation_alias="externalId")
    description: Optional[str] = None
    country_code: str = Field(validation_alias="countryCode")
    city_or_region: str = Field(validation_alias="cityOrRegion")
    endpoint_url: Optional[str] = Field(default=None, validation_alias="endpointUrl")
    resources: List[ResourceResponseObj] = []
