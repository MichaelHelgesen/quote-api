from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    #quote_id = db.Column(db.Integer(), db.ForeignKey("quotes.id"), nullable=False)

    #quote = db.relationship("QuoteModel", back_populates="tags")

    quote = db.relationship("QuoteModel", back_populates="tags", secondary="quote_tags")
