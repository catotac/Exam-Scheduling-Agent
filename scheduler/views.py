from django.shortcuts import render

from .models import *


def index(request):
    # Query model (Show TA-Exam Relation)
    ta_exam = TAExam.objects.all()

    # Create context to render
    context = {'ta_exam': ta_exam}
    return render(request, 'index.html', context)


def buildings(request):
    # Query model
    obj_list = Building.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'buildings/index.html', context)
