
from db import db

class PersonModel(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quote = db.relationship("QuoteModel", back_populates="quote", lazy="dynamic")
