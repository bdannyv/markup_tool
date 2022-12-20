import json
import logging

from django.contrib.auth.models import User
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(['POST'])
def signup(request):
    body_unicode = request.body.decode('utf-8')  # TODO: make a decorator to parse and validate input
    body = json.loads(body_unicode)

    user_id = body['user_id']
    username = body['username']
    password = body['password']  # TODO: Is it legal?
    email = body['email']

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
def signin(request):
    body_unicode = request.body.decode('utf-8')  # TODO: make a decorator to parse and validate input
    logging.error(body_unicode)
    body = json.loads(body_unicode)
    logging.error(body)

    user_id = body['user_id']
    password = body['password']  # TODO: Is it legal?

    # TODO: Too many responsibilities
    user = User.objects.filter(pk=user_id)
    if not user.count():
        return response.HttpResponse(status=401)

    authentication = user.first().check_password(raw_password=password)
    if not authentication:
        return response.HttpResponse(status=401)

    return response.HttpResponse(status=200)
