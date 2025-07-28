from extensions import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    shipping_address = db.Column(db.Sring(200))

    orders = db.relationship('Order', backref='client', lazy=True)
    comments = db.relationship('Comment', backref='client', lazy=True)

    def __repr__(self):
        return f"<Client {self.username}>"
