from functools import wraps

from flask import request, current_app
from sqlalchemy.orm.collections import InstrumentedList
from marshmallow import Schema, post_dump, pre_load, fields, ValidationError

from hyperion.common.utils import camelize, underscore


class HyperionSchema(Schema):
    """
    Base schema from which all grouper schema's inherit
    """

    __envelope__ = True

    def under(self, data, many=None):
        items = []
        if many:
            for i in data:
                items.append({underscore(key): value for key, value in i.items()})
            return items
        return {underscore(key): value for key, value in data.items()}

    def camel(self, data, many=None):
        items = []
        if many:
            for i in data:
                items.append(
                    {
                        camelize(key, uppercase_first_letter=False): value
                        for key, value in i.items()
                    }
                )
            return items
        return {
            camelize(key, uppercase_first_letter=False): value
            for key, value in data.items()
        }

    def wrap_with_envelope(self, data, many):
        if many:
            if "total" in self.context.keys():
                return dict(total=self.context["total"], items=data)
        return data


class HyperionInputSchema(HyperionSchema):
    @pre_load(pass_many=True)
    def preprocess(self, data, many, *args, **kwargs):
        return self.under(data, many=many)


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
        if data:
            data = self.camel(data, many=many)
        if self.__envelope__:
            return self.wrap_with_envelope(data, many=many)
        else:
            return data


def format_errors(messages):
    errors = {}
    for k, v in messages.items():
        key = camelize(k, uppercase_first_letter=False)
        if isinstance(v, dict):
            errors[key] = format_errors(v)
        elif isinstance(v, list):
            errors[key] = v[0]
    return errors


def wrap_errors(messages):
    errors = dict(message="Validation Error.")
    if messages.get("_schema"):
        errors["reasons"] = {"Schema": {"rule": messages["_schema"]}}
    else:
        errors["reasons"] = format_errors(messages)
    return errors


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
                    return wrap_errors(ex.messages), 400

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
