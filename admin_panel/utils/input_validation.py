import json
import logging
from functools import wraps
from typing import Type

from django.http import response
from pydantic import BaseModel, ValidationError


def request_body_validation(model: Type[BaseModel]):
    """Validation of request body"""
    def inner(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            body = json.loads(request.body)

            try:
                validated = model(**body)
            except ValidationError:
                logging.exception('HERE')
                return response.HttpResponse(status=400)

            kwargs['body'] = validated

            result = func(request, *args, **kwargs)
            return result

        return wrapper
    return inner
