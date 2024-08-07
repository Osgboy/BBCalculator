from django.urls import path
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Progress
import json
from . import views

async def get_progress(request, pID):
    p = await Progress.objects.aget(id=pID)
    progressState = {
        'progress': p.progress,
        'max_progress': p.max_progress
    }
    print(f'Task: {pID} with progress of {p.progress}/{p.max_progress}')
    return HttpResponse(json.dumps(progressState), content_type='application/json')


urlpatterns = [
    path('', views.index, name='index'),
    path('progress/<int:pID>/', get_progress, name='progress_status')
]