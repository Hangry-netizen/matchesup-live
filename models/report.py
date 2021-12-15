from models.base_model import BaseModel
import peewee as pw
from models.gsc import Gsc

class Report(BaseModel):
    reported_by = pw.ForeignKeyField(Gsc, backref="reported_by", on_delete="CASCADE")
    report_target = pw.ForeignKeyField(Gsc, backref="report_target", on_delete="CASCADE")
    reason = pw.TextField()
    recommended_action = pw.TextField(null=True)
    admin_remarks = pw.TextField(null=True)
    resolved = pw.BooleanField(default=False)