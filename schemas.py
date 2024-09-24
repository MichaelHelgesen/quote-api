from marshmallow import Schema, fields

class QuoteSchema(Schema):
    id = fields.Str(dump_only=True)
    quote = fields.Str(required=True)
    source = fields.Str()
    person_id = fields.Str(required=True)

class QuoteUpdateSchema(Schema):
    quote = fields.Str()
    source = fields.Str()

class PersonSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

