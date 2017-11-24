from django import forms

from datetime import datetime, timedelta


class DatagenForm(forms.Form):
    # Buildings
    building_instances = forms.IntegerField(label='Number of BUILDINGS', initial=5)
    coord_start = forms.FloatField(label='Random Coordinates Min Value', initial=-100.0)
    coord_end = forms.FloatField(label='Random Coordinates Max Value', initial=100.0)

    # Classrooms
    classroom_instances = forms.IntegerField(label='Number of CLASSROOMS', initial=10)
    classroom_capacity_min = forms.IntegerField(label='Min Room Capacity', initial=25)
    classroom_capacity_max = forms.IntegerField(label='Max Room Capacity', initial=250)
    classroom_ta_max = forms.IntegerField(label='Maximum TA Allocation', initial=3)
    classroom_num_schedules = forms.IntegerField(label='Number of MIDTERM SCHEDULES for each CL', initial=5)
    classroom_schedule_min_time = forms.DateTimeField(label='Midterm Schedule Start Date/Time',
                                                      initial=datetime.now(),
                                                      widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                                      input_formats=['%Y-%m-%d %I:%M %p'])
    classroom_schedule_max_time = forms.DateTimeField(label='Midterm Schedule End Date/Time',
                                                      initial=datetime.now()+timedelta(weeks=2),
                                                      widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                                      input_formats=['%Y-%m-%d %I:%M %p'])
    classroom_schedule_min = forms.IntegerField(label='Min Duration', initial=60)
    classroom_schedule_max = forms.IntegerField(label='Max Duration', initial=180)
    classroom_num_schedules_final = forms.IntegerField(label='Number of FINAL SCHEDULES for each CL', initial=5)
    classroom_schedule_min_time_final = forms.DateTimeField(label='Final Schedule Start Date/Time',
                                                            initial=datetime.now()+timedelta(weeks=8),
                                                            widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                                            input_formats=['%Y-%m-%d %I:%M %p'])
    classroom_schedule_max_time_final = forms.DateTimeField(label='Final Schedule End Date/Time',
                                                            initial=datetime.now()+timedelta(weeks=10),
                                                            widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                                            input_formats=['%Y-%m-%d %I:%M %p'])
    classroom_schedule_min_final = forms.IntegerField(label='Min Duration', initial=60)
    classroom_schedule_max_final = forms.IntegerField(label='Max Duration', initial=180)

    # Courses
    course_instances = forms.IntegerField(label='Number of COURSES', initial=5)
    course_capacity_min = forms.IntegerField(label='Min Course Capacity', initial=35)
    course_capacity_max = forms.IntegerField(label='Max Course Capacity', initial=500)

    # TAs
    ta_instances = forms.IntegerField(label='Number of TAs', initial=10)
    ta_num_schedules = forms.IntegerField(label='Number of SCHEDULES for each TA', initial=10)
    ta_schedule_min_time = forms.DateTimeField(label='Schedule Start Date/Time',
                                               initial=datetime.now(),
                                               widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                               input_formats=['%Y-%m-%d %I:%M %p'])
    ta_schedule_max_time = forms.DateTimeField(label='Schedule End Date/Time',
                                               initial=datetime.now()+timedelta(weeks=10),
                                               widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %I:%M %p'),
                                               input_formats=['%Y-%m-%d %I:%M %p'])
    ta_schedule_min = forms.IntegerField(label='Min Duration', initial=60)
    ta_schedule_max = forms.IntegerField(label='Max Duration', initial=180)
