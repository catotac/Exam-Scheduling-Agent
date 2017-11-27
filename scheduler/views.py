from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404

from datetime import datetime, timedelta
from pytz import timezone
import coms572_final.settings as settings

from datagen import Scheduler as sgen

from .models import *
from .forms import DatagenForm, ExamgenForm

from algorithm import Greedy


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


def building(request, obj_id):
    try:
        current_building = Building.objects.get(pk=obj_id)
    except Building.DoesNotExist:
        raise Http404("The building requested does not exist!")
    bl_ta = TA.objects.all().filter(building=current_building)
    bl_cl = Classroom.objects.all().filter(building=current_building)

    # Create context to render
    context = {'building': current_building, 'ta_list': bl_ta, 'classroom_list': bl_cl}
    return render(request, 'buildings/detail.html', context)


def classrooms(request):
    # Query model
    obj_list = Classroom.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'classrooms/index.html', context)


def classroom(request, obj_id):
    try:
        current_classroom = Classroom.objects.get(pk=obj_id)
    except Classroom.DoesNotExist:
        raise Http404("The classroom requested does not exist!")
    cl_scheds = ClassroomSchedule.objects.all().filter(classroom=current_classroom)

    # Create context to render
    context = {'classroom': current_classroom, 'obj_list': cl_scheds}
    return render(request, 'classrooms/detail.html', context)


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


def exam(request, obj_id):
    try:
        current_exam = Exam.objects.get(pk=obj_id)
    except Exam.DoesNotExist:
        raise Http404("The exam requested does not exist!")
    ta_list = TAExam.objects.all().filter(exam=current_exam)

    # Create context to render
    context = {'exam': current_exam, 'ta_list': ta_list}
    return render(request, 'exams/detail.html', context)


def tas(request):
    # Query model
    obj_list = TA.objects.all()

    # Create context to render
    context = {'obj_list': obj_list}
    return render(request, 'tas/index.html', context)


def ta(request, obj_id):
    try:
        current_ta = TA.objects.get(pk=obj_id)
    except TA.DoesNotExist:
        raise Http404("The TA requested does not exist!")
    ta_schedule = TASchedule.objects.all().filter(ta=current_ta)
    ta_course = TACourse.objects.all().filter(ta=current_ta)
    ta_exam = TAExam.objects.all().filter(ta=current_ta)

    # Create context to render
    context = {'ta': current_ta, 'schedule_list': ta_schedule, 'course_list': ta_course, 'exam_list': ta_exam}
    return render(request, 'tas/detail.html', context)


def generate_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DatagenForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Clean database
            Building.objects.all().delete()
            Classroom.objects.all().delete()
            ClassroomSchedule.objects.all().delete()
            TA.objects.all().delete()
            TASchedule.objects.all().delete()
            Course.objects.all().delete()
            Exam.objects.all().delete()
            TACourse.objects.all().delete()
            TAExam.objects.all().delete()

            # Generate buildings
            building_gen = sgen.BuildingGenerator(form.cleaned_data['building_instances'],
                                                  form.cleaned_data['coord_start'],
                                                  form.cleaned_data['coord_end'])
            obj_buildings = building_gen.generate()

            # Save object to the database
            for obj in obj_buildings:
                db_input = Building()
                db_input.id = obj['id']
                db_input.name = obj['name']
                db_input.coord_x = obj['coord_x']
                db_input.coord_y = obj['coord_y']
                db_input.save()

            # Generate classrooms and their schedules
            classroom_gen = sgen.ClassroomGenerator(obj_buildings,
                                                    form.cleaned_data['classroom_instances'],
                                                    form.cleaned_data['classroom_capacity_min'],
                                                    form.cleaned_data['classroom_capacity_max'],
                                                    form.cleaned_data['classroom_ta_max'])
            obj_classrooms = classroom_gen.generate()

            # Save object to the database
            for obj in obj_classrooms:
                db_input = Classroom()
                db_input.id = obj['id']
                db_input.name = obj['name']
                db_input.capacity = obj['capacity']
                db_input.max_ta = obj['max_ta']
                db_input.building_id = obj['building_id']
                db_input.save()

            # Classroom schedule should start at 8:00 AM and end at 5:00 PM
            cl_schedule_start = datetime.now(timezone(settings.TIME_ZONE))
            cl_schedule_start = cl_schedule_start.replace(hour=8, minute=0, second=0)
            cl_schedule_end = cl_schedule_start + timedelta(hours=9)

            classroom_schedgen = sgen.ScheduleGenerator(len(obj_classrooms),
                                                        form.cleaned_data['classroom_num_schedules'],
                                                        form.cleaned_data['classroom_schedule_min_time'],
                                                        form.cleaned_data['classroom_schedule_max_time'],
                                                        form.cleaned_data['classroom_schedule_min'],
                                                        form.cleaned_data['classroom_schedule_max'])
            obj_cl_scheds = classroom_schedgen.generate()

            # Save object to the database
            for obj in obj_cl_scheds:
                db_input = ClassroomSchedule()
                db_input.id = obj['id']
                db_input.start_time = obj['start_time']
                db_input.end_time = obj['end_time']
                db_input.classroom_id = obj['parent_id']
                db_input.save()

            classroom_schedgen_final = sgen.ScheduleGenerator(len(obj_classrooms),
                                                              form.cleaned_data['classroom_num_schedules_final'],
                                                              form.cleaned_data['classroom_schedule_min_time_final'],
                                                              form.cleaned_data['classroom_schedule_max_time_final'],
                                                              form.cleaned_data['classroom_schedule_min_final'],
                                                              form.cleaned_data['classroom_schedule_max_final'])
            obj_cl_scheds_final = classroom_schedgen_final.generate(cl_schedule_start, cl_schedule_end)

            # Save object to the database
            for obj in obj_cl_scheds_final:
                db_input = ClassroomSchedule()
                db_input.id = obj['id']
                db_input.start_time = obj['start_time']
                db_input.end_time = obj['end_time']
                db_input.classroom_id = obj['parent_id']
                db_input.save()

            # Generate courses
            course_gen = sgen.CourseGenerator(obj_buildings,
                                              form.cleaned_data['course_instances'],
                                              form.cleaned_data['course_capacity_min'],
                                              form.cleaned_data['course_capacity_max'])
            obj_courses = course_gen.generate()

            # Save object to the database
            for obj in obj_courses:
                db_input = Course()
                db_input.id = obj['id']
                db_input.code = obj['code']
                db_input.capacity = obj['capacity']
                db_input.building_id = obj['building_id']
                db_input.save()

            # Generate TAs and their schedules
            ta_gen = sgen.TAGenerator(obj_buildings,
                                      form.cleaned_data['ta_instances'])
            obj_tas = ta_gen.generate()

            # Save object to the database
            for obj in obj_tas:
                db_input = TA()
                db_input.id = obj['id']
                db_input.first_name = obj['first_name']
                db_input.last_name = obj['last_name']
                db_input.email = obj['email']
                db_input.building_id = obj['building_id']
                db_input.save()

            # # TA schedule should start from 9:00 AM and end at 9:00 PM
            # ta_schedule_start = datetime.now(timezone(settings.TIME_ZONE))
            # ta_schedule_start = ta_schedule_start.replace(hour=9, minute=0, second=0)
            # ta_schedule_end = ta_schedule_start + timedelta(hours=12)
            #
            # ta_schedgen = sgen.ScheduleGenerator(len(obj_tas),
            #                                      form.cleaned_data['ta_num_schedules'],
            #                                      form.cleaned_data['ta_schedule_min_time'],
            #                                      form.cleaned_data['ta_schedule_max_time'],
            #                                      form.cleaned_data['ta_schedule_min'],
            #                                      form.cleaned_data['ta_schedule_max'])
            # obj_ta_scheds = ta_schedgen.generate(ta_schedule_start, ta_schedule_end)
            #
            # # Save object to the database
            # for obj in obj_ta_scheds:
            #     db_input = TASchedule()
            #     db_input.id = obj['id']
            #     db_input.start_time = obj['start_time']
            #     db_input.end_time = obj['end_time']
            #     db_input.ta_id = obj['parent_id']
            #     db_input.save()

            # redirect to the home page:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DatagenForm()

    return render(request, 'datagen.html', {'form': form})


def truncate_db(request):
    Building.objects.all().delete()
    Classroom.objects.all().delete()
    ClassroomSchedule.objects.all().delete()
    TA.objects.all().delete()
    TASchedule.objects.all().delete()
    Course.objects.all().delete()
    Exam.objects.all().delete()
    TACourse.objects.all().delete()
    TAExam.objects.all().delete()

    return HttpResponseRedirect('/')


def assign_ta(request):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ExamgenForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # INFO: Date objects corresponding to the user input are:
            #   form.cleaned_data['midterm_start_date']
            #   form.cleaned_data['midterm_end_date']
            #   form.cleaned_data['final_start_date']
            #   form.cleaned_data['final_end_date']

            #
            # The algorithms should be called here #
            #

            # Call Rahul's algorithm
            Greedy.run_algorithm(form.cleaned_data['midterm_start_date'],
                                 form.cleaned_data['midterm_end_date'],
                                 form.cleaned_data['final_start_date'],
                                 form.cleaned_data['final_end_date'])

            # Redirect to the home page:
            return HttpResponseRedirect('/')

    # If a GET (or any other method) we'll create a blank form
    else:
        form = ExamgenForm()

    return render(request, 'examgen.html', {'form': form})
