from pydantic import BaseModel, ConfigDict


class DiseaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    color_hex: str
    description: str
