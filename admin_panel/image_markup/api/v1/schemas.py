from pydantic import BaseModel


class LabelInputBaseModel(BaseModel):
    user_id: int
    image_id: str
    type: str
