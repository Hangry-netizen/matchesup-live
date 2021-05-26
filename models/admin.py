from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re

class Admin(BaseModel):
  username = pw.CharField(unique=True)
  password_hash = pw.CharField(unique=True)
  password = None

  def validate(self):
    duplicate_username = Admin.get_or_none(Admin.username == self.username)
    
    if duplicate_username and self.id != duplicate_username.id:
      self.errors.append("There is an existing account with this username")

    if self.password:
      if len(self.password) < 6:
        self.errors.append("Password must consist of at least 6 characters")
      if len(self.errors) == 0:
        self.password_hash = generate_password_hash(self.password)
    elif not self.password_hash:
      self.errors.append("Password is required")