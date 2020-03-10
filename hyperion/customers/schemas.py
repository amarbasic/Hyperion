from marshmallow import Schema, fields

from hyperion.common.schema import HyperionOutputSchema


class CustomerListDetailsSchema(HyperionOutputSchema):
    id = fields.Integer()
    name = fields.String()
    is_active = fields.Boolean()
