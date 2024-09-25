from db import db

class QuoteModel(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), unique=True, nullable=False)
    source = db.Column(db.String(80), unique=False, nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), unique=False, nullable=False)
    person = db.relationship("PersonModel", back_populates="quote")
    #tags = db.relationship("TagModel", back_populates="quote", lazy="dynamic")
    tags = db.relationship("TagModel", back_populates="quote", secondary="quote_tags")
