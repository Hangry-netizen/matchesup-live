from models.base_model import BaseModel
import peewee as pw
from models.gsc import Gsc

class Hello(BaseModel):
    said_hi = pw.ForeignKeyField(Gsc, backref="said_hi", on_delete="CASCADE")
    hi_recipient = pw.ForeignKeyField(Gsc, backref="hi_recipient", on_delete="CASCADE")
    contacted = pw.BooleanField(default=False)
    removed = pw.BooleanField(default=False)