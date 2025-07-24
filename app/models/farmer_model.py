from app import db  # ✅ Make sure this is at the top

class Farmer(db.Model):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text, nullable=True)  # ✅ new line for farmer note

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "contact": self.contact,
            "username": self.username,
            "password": self.password,
            "note": self.note  # ✅ include it in output
        }
