import json

from authapp.api.v1.schemas import SignInBodyModel, SignUpBodyModel
from django.contrib.auth import authenticate, models
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from utils.input_validation import request_body_validation


@csrf_exempt
@require_http_methods(['POST'])
@request_body_validation(model=SignUpBodyModel)
def signup(request, body: SignUpBodyModel):

    user = models.User.objects.filter(username=body.username)
    if user:
        return response.HttpResponse(
            status=409, content=json.dumps({'message': 'already signed up'}), content_type="application/json"
        )

    models.User.objects.create_user(username=body.username, password=body.password, email=body.email)

    return response.HttpResponse(
        status=200, content=json.dumps({'message': 'successfully signed up'}), content_type="application/json"
    )


@csrf_exempt
@require_http_methods(['POST'])
@request_body_validation(model=SignInBodyModel)
def signin(request, body: SignInBodyModel):
    user = models.User.objects.filter(username=body.username)

    if not user.count():
        return response.HttpResponse(status=401)

    authentication = authenticate(username=body.username, password=body.password)
    if not authentication:
        return response.HttpResponse(status=401)

    return response.HttpResponse(status=200)
