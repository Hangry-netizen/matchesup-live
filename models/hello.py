from models.base_model import BaseModel
import peewee as pw
from models.gsc import Gsc

class Hello(BaseModel):
    said_hi = pw.ForeignKeyField(Gsc, backref="said_hi", on_delete="CASCADE")
    hi_recipient = pw.ForeignKeyField(Gsc, backref="hi_recipient", on_delete="CASCADE")
    contacted = pw.BooleanField(default=False)
    removed = pw.BooleanField(default=False)

    def validate(self):
        duplicate_hello = Hello.get_or_none(Hello.said_hi == self.said_hi and Hello.hi_recipient == self.hi_recipient)

        if duplicate_hello and self.id != duplicate_hello.id:
            self.errors.append("You have said hi to this profile!")