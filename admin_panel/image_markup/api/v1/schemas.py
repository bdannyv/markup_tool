from pydantic import BaseModel


class LabelInputBaseModel(BaseModel):
    user_name: str
    image_id: str
    type: str
