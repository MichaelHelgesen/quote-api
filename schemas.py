from marshmallow import Schema, fields

class PlainQuoteSchema(Schema):
    id = fields.Int(dump_only=True)
    quote = fields.Str(required=True)
    source = fields.Str()

class PlainPersonSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class QuoteUpdateSchema(Schema):
    quote = fields.Str()
    source = fields.Str()
    person_id = fields.Int()

class QuoteSchema(PlainQuoteSchema):
    person_id = fields.Int(required=True, load_only=True)
    person = fields.Nested(PlainPersonSchema(), dump_only=True)
    #tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
class PersonSchema(PlainPersonSchema):
    quotes = fields.List(fields.Nested(PlainQuoteSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    #quote_id = fields.Int(load_only=True)
    #quote = fields.Nested(PlainQuoteSchema(), dump_only=True)
    quote = fields.List(fields.Nested(PlainQuoteSchema()), dump_only=True)


class TagAndQuoteSchema(Schema):
    message = fields.Str()
    quote = fields.Nested(QuoteSchema)
    tags = fields.Nested(TagSchema)

