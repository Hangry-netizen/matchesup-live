from models.base_model import BaseModel
import peewee as pw


class SingleCommunities(BaseModel):
    email = pw.CharField()