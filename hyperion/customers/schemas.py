from marshmallow import Schema, fields, validates, ValidationError

from hyperion.common.schema import HyperionOutputSchema, HyperionInputSchema


class CustomerListDetailsSchema(HyperionOutputSchema):
    id = fields.Integer()
    name = fields.String()
    is_active = fields.Boolean()


class CustomerCreateSchema(HyperionInputSchema):
    name = fields.String(required=True)
    is_active = fields.Boolean(required=True)

    @validates("name")
    def validate_name(self, value):
        if len(value) > 25:
            raise ValidationError("Name must be less than 25 characters")

        if len(value) < 5:
            raise ValidationError("Name must be greater than 5 characters")
