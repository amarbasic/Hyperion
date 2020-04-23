from functools import wraps

from flask import request
from sqlalchemy.orm.collections import InstrumentedList
from marshmallow import Schema, post_dump, pre_load, fields, ValidationError


# TODO: Move to common
def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class HyperionSchema(Schema):
    __envelope__ = True

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    def wrap_with_envelope(self, data, many):
        if many:
            if "total" in self.context.keys():
                return dict(total=self.context["total"], items=data)
        return data


class HyperionInputSchema(HyperionSchema):
    pass


class HyperionOutputSchema(HyperionSchema):
    @pre_load(pass_many=True)
    def preprocess(self, data, many):
        if many:
            data = self.unwrap_envelope(data, many)
        return self.under(data, many=many)

    def unwrap_envelope(self, data, many):
        if many:
            if data["items"]:
                if isinstance(data, InstrumentedList) or isinstance(data, list):
                    self.context["total"] = len(data)
                    return data
                else:
                    self.context["total"] = data["total"]
            else:
                self.context["total"] = 0
                data = {"items": []}

            return data["items"]

        return data

    @post_dump(pass_many=True)
    def post_process(self, data, many):
        if self.__envelope__:
            return self.wrap_with_envelope(data, many=many)
        else:
            return data


# TODO: Drop this
def unwrap_pagination(data, output_schema):
    if not output_schema:
        return data

    if isinstance(data, dict):
        if "total" in data.keys():
            if data.get("total") == 0:
                return data

            marshaled_data = {"total": data["total"]}
            marshaled_data["items"] = output_schema.dump(data["items"], many=True)
            return marshaled_data

        return output_schema.dump(data)

    elif isinstance(data, list):
        marshaled_data = {"total": len(data)}
        marshaled_data["items"] = output_schema.dump(data, many=True)
        return marshaled_data

    return output_schema.dump(data)


def validate_schema(
    input_schema: HyperionInputSchema = None, output_schema: HyperionOutputSchema = None
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if input_schema:
                if callable(input_schema):
                    input_schema_to_use = input_schema()
                else:
                    input_schema_to_use = input_schema

                if request.get_json():
                    request_data = request.get_json()
                else:
                    request_data = request.args

                try:
                    data = input_schema_to_use.load(request_data)
                except ValidationError as ex:
                    return ex.messages, 400

                kwargs["data"] = data

            resp = f(*args, **kwargs)
            response_data = resp
            status = 200

            if isinstance(resp, tuple):
                response_data = resp[0]
                status = resp[1]

            if callable(output_schema):
                output_schema_to_use = output_schema()
            else:
                output_schema_to_use = output_schema

            return unwrap_pagination(response_data, output_schema_to_use), status

        return decorated_function

    return decorator
