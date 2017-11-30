from scheduler import models

import random
import copy
from datetime import date, datetime, time, timedelta
from pytz import timezone

import coms572_final.settings as settings


def run_algorithm(midterm_start, midterm_end, final_start, final_end):
    # midterm_* and final_* vars are date object
    # example: midterm_start is an date object
    #print("I AM HERE")
    ta_list = models.TA.objects.all()
    classroom_list = models.Classroom.objects.all()
    course_list_orig = list(models.Course.objects.all())
    types = ['MIDTERM', 'FINAL']
    timeslots = [time(i, 0, tzinfo=timezone(settings.TIME_ZONE)) for i in range(time(8, 0, tzinfo=timezone(settings.TIME_ZONE)).hour, time(17, 0, tzinfo=timezone(settings.TIME_ZONE)).hour + 1)]
   # timeslots = [time(i, 0) for i in range(time(8, 0).hour, time(17, 0).hour + 1)]
    midtermdays = []
    finaldays = []
    delta = midterm_end - midterm_start  # timedelta
    for i in range(delta.days + 1):
        midtermdays.append(midterm_start + timedelta(days=i))
    delta = final_end - final_start  # timedelta
    for i in range(delta.days + 1):
        finaldays.append(final_start + timedelta(days=i))
    ta_examlist = []
    for typ in types:
        exam_schedule = []
        listofschedules = []
        temp_talist = []
        counter = 0
        if typ is 'MIDTERM':
            examdays = midtermdays
        else:
            examdays = finaldays
        course_list = copy.deepcopy(course_list_orig)
        while(len(course_list) is not 0):
            maxClass = max(course_list, key=lambda x: x.capacity)
            #print(maxClass)
            #print("MAXCLASS")
            day = random.choice(examdays)
            startTime = random.choice(timeslots)
            listofclassrooms = assignclassroom(maxClass, classroom_list, day, startTime, listofschedules)
            start_time = datetime.combine(day, startTime)
           # start_time = start_time.replace(tzinfo=timezone(settings.TIME_ZONE))
      #      start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.combine(day, startTime) + timedelta(hours=2)
            #end_time = end_time.replace(tzinfo=timezone(settings.TIME_ZONE))
       #     end_time.strftime('%Y-%m-%d %H:%M:%S')
            dbq = models.Exam()
            dbq.start_time = start_time
            dbq.end_time = end_time
            dbq.type = typ
            dbq.course_id = maxClass.id
            # print(examtype['course_id'])
            dbq.save()
            exam_list = models.Exam.objects.all()
            examID = gettheexamID(exam_list, maxClass.id, typ)
            listoftas = assignTAs(maxClass, ta_list, listofclassrooms, examID, day, startTime, listofschedules, ta_examlist, temp_talist)
            temp = {'id': counter,
                    'startTime': startTime,
                    'day':day,
                    'classroomlist':listofclassrooms,
                    'talist':listoftas
                    }
            # temp1 = {'start_time': start_time,
            #          'end_time':end_time,
            #          'type':typ,
            #          'course_id':maxClass.id
            #          }
            #print(temp1)
            #exam_schedule.append(temp1)
            listofschedules.append(temp)
            course_list.remove(maxClass)
            counter = counter + 1
    saveTAexamtodatabase(ta_examlist)




def assignTAs(coursenum, taslist_old, classroom_list_old, counter, day, startTime, listofschedules_old, ta_examlist, temp_talist):
    classroom_list = classroom_list_old[:]
    listofschedules = listofschedules_old[:]
    course = copy.copy(coursenum)
    taslist = taslist_old[:]
    retlist = []
    tasinsamebuilding = []
    tasnotinsamebuilding = []
    roomsinsamebuilding = []
    roomsnotinsamebuilding = []
    for tas in taslist:
        if course.building_id == tas.building_id:
            tasinsamebuilding.append(tas)
        else:
            tasnotinsamebuilding.append(tas)
    tasinsamebuilding.extend(tasnotinsamebuilding)
    for classroom in classroom_list:
        if course.building_id == classroom.building_id:
            roomsinsamebuilding.append(classroom)
        else:
            roomsnotinsamebuilding.append(classroom)
    roomsinsamebuilding.extend(roomsnotinsamebuilding)
    counter_ta = 0
    counter_room = 0
    while(len(roomsinsamebuilding) > 0):
        if (len(tasinsamebuilding) - 1) == counter_ta:
            temp_talist.clear()
            counter_ta = 0
        classroom = roomsinsamebuilding[counter_room]
        ta = tasinsamebuilding[counter_ta]
        if availofTA(ta, day, startTime, listofschedules):
            if(temp_talist.__contains__(ta)):
                counter_ta = counter_ta + 1
                continue
            else:
                temp = {'classroom_id':classroom.id,
                        'exam_id':counter,
                        'ta_id':ta.id
                        }
                ta_examlist.append(temp)
                retlist.append(ta)
                roomsinsamebuilding.remove(classroom)
        #       counter_room = counter_room + 1
                temp_talist.append(ta)
                counter_ta = counter_ta + 1
        else:
            counter_ta = counter_ta + 1
    #print(course)
    #print("HERE I AM in TA")
    #print(ta_examlist)
    #print("I AM in TA")
    return retlist


def assignclassroom(coursenum, classroom_list_old, day, startTime, listofschedules_old):
    classroom_list = classroom_list_old[:]
    listofschedules = listofschedules_old[:]
    course = copy.copy(coursenum)
    retlist = []
    roomsinsamebuilding = []
    roomsnotinsamebuilding = []
    for classroom in classroom_list:
        if course.building_id == classroom.building_id:
            roomsinsamebuilding.append(classroom)
        else:
            roomsnotinsamebuilding.append(classroom)
    while(len(roomsinsamebuilding) > 0 and course.capacity > 0):
        maxcapacityclassroom = max(roomsinsamebuilding, key=lambda x: x.capacity)
        if availofclassroom(maxcapacityclassroom, day, startTime, listofschedules):
           retlist.append(maxcapacityclassroom)
           roomsinsamebuilding.remove(maxcapacityclassroom)
           course.capacity = course.capacity - maxcapacityclassroom.capacity
        else:
            roomsinsamebuilding.remove(maxcapacityclassroom)
    if(course.capacity <  0):
  #      print(course)
  #      print("HERE I AM IN ASSIGN COURSES")
  #      print(retlist)
        return retlist
    else:
        while (len(roomsnotinsamebuilding) > 0 and course.capacity > 0):
            maxcapacityclassroom = max(roomsnotinsamebuilding, key=lambda x: x.capacity)
            if availofclassroom(maxcapacityclassroom, day, startTime, listofschedules):
                retlist.append(maxcapacityclassroom)
                roomsnotinsamebuilding.remove(maxcapacityclassroom)
                course.capacity = course.capacity - maxcapacityclassroom.capacity
            else:
                roomsnotinsamebuilding.remove(maxcapacityclassroom)
 #   print(course)
 #   print("HERE I AM IN ASSIGN COURSES")
    return retlist


def availofclassroom(classroom, day, startTime, listofschedules):
    if len(listofschedules) == 0:
        return True
    else:
        for exam in listofschedules:
            if day == exam['day'] and startTime == exam['startTime']:
                if classroom in exam['classroomlist']:
                    return False
    return True


def availofTA(ta, day, startTime, listofschedules):
    if len(listofschedules) == 0:
        return True
    else:
        for exam in listofschedules:
            if day == exam['day'] and startTime == exam['startTime']:
                if ta in exam['talist']:
                    return False
    return True


def saveexamtypetodatabase(examtypelist):
    for examtype in examtypelist:
        dbq = models.Exam()
        dbq.start_time = examtype['start_time']
        dbq.end_time = examtype['end_time']
        dbq.type = examtype['type']
        dbq.course_id = examtype['course_id']
        #print(examtype['course_id'])
        dbq.save()


def saveTAexamtodatabase(taexamlist):
    for taexamtype in taexamlist:
        dbq = models.TAExam()
        dbq.classroom_id = taexamtype['classroom_id']
        dbq.exam_id = taexamtype['exam_id']
        dbq.ta_id = taexamtype['ta_id']
        dbq.save()


def gettheexamID(examlist, id, typ):
    for exams in examlist:
        if id == exams.course_id and typ == exams.type:
            return exams.id


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


