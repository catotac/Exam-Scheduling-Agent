from scheduler import models

from datetime import datetime, date, time, timedelta


def test_function(midterm_start, midterm_end, final_start, final_end):
    # midterm_* and final_* vars are date objects
    # example: midterm_start is an date object
    ta_list = models.TA.objects.all()
    for ta in ta_list:
        # ta is your TA class in models.py
        # ta.first_name, ta.last_time, etc.
        pass

    classroom_list = models.Classroom.objects.all()

    for cl in classroom_list:
        schedule = models.ClassroomSchedule.objects.all().filter(classroom=cl)
        for sched in schedule:
            # sched.start_time as a datetime object
            pass

    # Save to DB
    dbq = models.TAExam()
    dbq.classroom_id = 1
    dbq.exam_id = 2
    dbq.save()
