from django.shortcuts import render

from .models import Building


def index(request):
    # Create context to render
    context = { }
    return render(request, 'index.html', context)


def buildings(request):
    # Query model
    building_list = Building.objects.all()

    # Create context to render
    context = {'building_list': building_list}
    return render(request, 'buildings/index.html', context)
