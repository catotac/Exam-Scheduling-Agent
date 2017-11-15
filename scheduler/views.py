from django.shortcuts import render
from django.http import HttpResponse

from .models import Building


def index(request):
    return HttpResponse("Hello, world. You're at the Scheduler index.")


def buildings(request):
    # Query model
    building_list = Building.objects.all()

    # Create context to render
    context = {'building_list': building_list}
    return render(request, 'buildings/index.html', context)
