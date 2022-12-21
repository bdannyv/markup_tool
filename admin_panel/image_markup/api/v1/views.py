# Create your views here.
import json
import os

from config.settings import MEDIA_ROOT
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from image_markup.api.v1 import schemas
from image_markup.models import ImageClass, ImageTable, Label
from utils.input_validation import request_body_validation


@staff_member_required
@require_http_methods(["GET"])
def statistics_view(request):
    """Statistics view"""
    test = Label.objects.values('type__name').annotate(Count('id'))

    return render(
        request,
        context={
            'obj_total': ImageTable.objects.count(),
            'labeled': Label.objects.select_related('image').count(),
            'classes': test,
        },
        template_name='markup/index.html'
    )


@require_http_methods(['GET'])
def get_classes(request):
    q = ImageClass.objects.values('name').all()

    if not q:
        return response.HttpResponse(status=204)

    return response.HttpResponse(
        status=200,
        content_type='application/json',
        content=json.dumps([row['name'] for row in q])
    )


@require_http_methods(["GET"])
def get_unlabeled_image_id(request):
    """Get unlabeled message"""
    q = ImageTable.objects.filter(image_class__isnull=True).first()

    if not q:
        return response.HttpResponse(status=204)

    return response.HttpResponse(
        status=200,
        content_type="application/json",
        content=json.dumps({'id': str(q.id), "name": q.image.name}))


@require_http_methods(["GET"])
def get_image(request, id):
    q = ImageTable.objects.filter(id=id).values('image').first()

    if not q:
        return response.HttpResponse(status=404)

    with open(os.path.join(MEDIA_ROOT, q["image"]), 'rb') as image:
        return response.HttpResponse(image, content_type="image/jpeg")


@csrf_exempt
@require_http_methods(['POST'])
@request_body_validation(model=schemas.LabelInputBaseModel)
def labeled_image(request, body: schemas.LabelInputBaseModel):
    """Label image view"""
    i_class = ImageClass.objects.filter(name=body.type).first()
    if not i_class:
        return response.HttpResponse(
            status=400,
            content=json.dumps({"message": "Unknown label type"}),
            content_type='application/json'
        )

    img = ImageTable.objects.filter(id=body.image_id).first()
    if not img:
        return response.HttpResponse(
            status=400,
            content=json.dumps({"message": "Image not found"}),
            content_type='application/json'
        )

    user = User.objects.filter(username=body.user_name).first()
    if not user:
        return response.HttpResponse(
            status=401,
            content=json.dumps({"message": "Image not found"}),
            content_type='application/json'
        )

    label = Label(
        type=i_class,
        image=img,
        user=user
    )
    label.save()

    return response.HttpResponse(status=200)
