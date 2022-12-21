import json

from authapp.api.v1.schemas import SignInBodyModel, SignUpBodyModel
from django.contrib.auth.models import User
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from utils.input_validation import request_body_validation


@csrf_exempt
@require_http_methods(['POST'])
@request_body_validation(model=SignUpBodyModel)
def signup(request, body: SignUpBodyModel):

    user_id = body.user_id
    username = body.username
    password = body.password  # TODO: Is it legal?
    email = body.email

    # TODO: Too many responsibilities
    user = User.objects.filter(id=user_id)
    if user:
        return response.HttpResponse(
            status=409, content=json.dumps({'message': 'already signed up'}), content_type="application/json"
        )

    User.objects.create_user(username=username, password=password, email=email, pk=user_id)

    return response.HttpResponse(
        status=200, content=json.dumps({'message': 'successfully signed up'}), content_type="application/json"
    )


@csrf_exempt
@require_http_methods(['POST'])
@request_body_validation(model=SignInBodyModel)
def signin(request, body: SignInBodyModel):

    user_id = body.user_id
    password = body.password  # TODO: Is it legal?

    # TODO: Too many responsibilities
    user = User.objects.filter(pk=user_id)
    if not user.count():
        return response.HttpResponse(status=401)

    authentication = user.first().check_password(raw_password=password)
    if not authentication:
        return response.HttpResponse(status=401)

    return response.HttpResponse(status=200)
