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


def classrooms(request):
    # Query model
    obj_list = Classroom.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'classrooms/index.html', context)


def courses(request):
    # Query model
    obj_list = Course.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'courses/index.html', context)


def exams(request):
    # Query model
    obj_list = Exam.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'exams/index.html', context)


def tas(request):
    # Query model
    obj_list = TA.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'tas/index.html', context)
