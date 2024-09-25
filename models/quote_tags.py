from db import db

class QuoteTags(db.Model):
    __tablename__ = "quote_tags"

    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey("quotes.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
