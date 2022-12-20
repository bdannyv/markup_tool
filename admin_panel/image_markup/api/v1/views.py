# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from image_markup.models import ImageTable, Label


@staff_member_required
@require_http_methods(["GET"])
def my_view(request):
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
