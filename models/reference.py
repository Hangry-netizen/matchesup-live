from models.base_model import BaseModel
import peewee as pw
from models.gsc import Gsc

class Reference(BaseModel):
    gsc = pw.ForeignKeyField(Gsc, backref="references", on_delete="CASCADE")
    ref_name = pw.CharField()
    ref_email = pw.CharField()
    reasons_gscf_makes_a_good_partner = pw.TextField(null=True)
    good_match_for_gscf = pw.TextField(null=True)
    is_approved = pw.BooleanField(default=False)