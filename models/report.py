from models.base_model import BaseModel
import peewee as pw
from models.gsc import Gsc

class Report(BaseModel):
    reported_by = pw.ForeignKeyField(Gsc, backref="reported_by", on_delete="CASCADE")
    report_target = pw.ForeignKeyField(Gsc, backref="report_target", on_delete="CASCADE")
    reason = pw.TextField()
    admin_remarks = pw.TextField(null=True)
    archived = pw.BooleanField(default=False)