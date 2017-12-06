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
    classroom_schedule_min_time = forms.DateField(label='Midterm Schedule Start Date',
                                                  initial=datetime.now().date(),
                                                  widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                                  input_formats=['%Y-%m-%d'])
    classroom_schedule_max_time = forms.DateField(label='Midterm Schedule End Date',
                                                  initial=datetime.now().date() + timedelta(weeks=2),
                                                  widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                                  input_formats=['%Y-%m-%d'])
    classroom_schedule_min = forms.IntegerField(label='Min Duration', initial=60)
    classroom_schedule_max = forms.IntegerField(label='Max Duration', initial=180)
    classroom_num_schedules_final = forms.IntegerField(label='Number of FINAL SCHEDULES for each CL', initial=5)
    classroom_schedule_min_time_final = forms.DateField(label='Final Schedule Start Date',
                                                        initial=datetime.now().date() + timedelta(weeks=8),
                                                        widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                                        input_formats=['%Y-%m-%d'])
    classroom_schedule_max_time_final = forms.DateField(label='Final Schedule End Date',
                                                        initial=datetime.now().date() + timedelta(weeks=10),
                                                        widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                                        input_formats=['%Y-%m-%d'])
    classroom_schedule_min_final = forms.IntegerField(label='Min Duration', initial=60)
    classroom_schedule_max_final = forms.IntegerField(label='Max Duration', initial=180)

    # Courses
    course_instances = forms.IntegerField(label='Number of COURSES', initial=5)
    course_capacity_min = forms.IntegerField(label='Min Course Capacity', initial=35)
    course_capacity_max = forms.IntegerField(label='Max Course Capacity', initial=500)

    # TAs
    ta_instances = forms.IntegerField(label='Number of TAs', initial=10)
    ta_num_schedules = forms.IntegerField(label='Number of SCHEDULES for each TA', initial=25)
    ta_schedule_min_time = forms.DateField(label='TA Schedule Start Date',
                                           initial=datetime.now().date(),
                                           widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                           input_formats=['%Y-%m-%d'])
    ta_schedule_max_time = forms.DateField(label='TA Schedule End Date/Time',
                                           initial=datetime.now().date() + timedelta(weeks=10),
                                           widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                           input_formats=['%Y-%m-%d'])
    ta_schedule_min = forms.IntegerField(label='Min Duration', initial=60)
    ta_schedule_max = forms.IntegerField(label='Max Duration', initial=180)


class TAAssignMainForm(forms.Form):
    # Midterm schedule
    midterm_start_date = forms.DateField(label='Midterm Schedule Start Date',
                                         initial=datetime.now().date(),
                                         widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                         input_formats=['%Y-%m-%d'])
    midterm_end_date = forms.DateField(label='Midterm Schedule End Date',
                                       initial=datetime.now().date() + timedelta(weeks=2),
                                       widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                       input_formats=['%Y-%m-%d'])

    # Final schedule
    final_start_date = forms.DateField(label='Final Schedule Start Date',
                                       initial=datetime.now().date() + timedelta(weeks=8),
                                       widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                       input_formats=['%Y-%m-%d'])
    final_end_date = forms.DateField(label='Final Schedule End Date',
                                     initial=datetime.now().date() + timedelta(weeks=10),
                                     widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                     input_formats=['%Y-%m-%d'])

    # Initial temperature for Simulated Annealing
    sa_initial_temp = forms.IntegerField(label='Initial Temperature', initial=100)
    sa_final_temp = forms.IntegerField(label='Final Temperature', initial=1)
    sa_num_rep = forms.IntegerField(label='Number of Repetitions', initial=3)
    sa_num_move = forms.IntegerField(label='Number of Movements', initial=5)


class GreedyAlgoForm(forms.Form):
    # Midterm schedule
    midterm_start_date = forms.DateField(label='Midterm Schedule Start Date',
                                         initial=datetime.now().date(),
                                         widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                         input_formats=['%Y-%m-%d'])
    midterm_end_date = forms.DateField(label='Midterm Schedule End Date',
                                       initial=datetime.now().date() + timedelta(weeks=2),
                                       widget=forms.widgets.DateInput(format='%Y-%m-%d'),
                                       input_formats=['%Y-%m-%d'])

    # Final schedule
    final_start_date = forms.DateField(label='Final Schedule Start Date',
                                       initial=datetime.now().date() + timedelta(weeks=8),
                                       widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                       input_formats=['%Y-%m-%d'])
    final_end_date = forms.DateField(label='Final Schedule End Date',
                                     initial=datetime.now().date() + timedelta(weeks=10),
                                     widget=forms.widgets.DateTimeInput(format='%Y-%m-%d'),
                                     input_formats=['%Y-%m-%d'])


class SAAlgoForm(forms.Form):
    sa_initial_temp = forms.IntegerField(label='Initial Temperature', initial=100)
    sa_final_temp = forms.IntegerField(label='Final Temperature', initial=1)
    sa_num_rep = forms.IntegerField(label='Number of Repetitions', initial=3)
    sa_num_move = forms.IntegerField(label='Number of Movements', initial=5)
