from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100)
    coord_x = models.FloatField(default=0.0)
    coord_y = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Building'
        verbose_name_plural = 'Buildings'


class Classroom(models.Model):
    name = models.CharField(max_length=100, default='Classroom')
    capacity = models.IntegerField()
    max_ta = models.PositiveIntegerField(verbose_name='Max Assignable TAs')
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'


class ClassroomSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Classroom Schedule'
        verbose_name_plural = 'Classroom Schedules'


class Course(models.Model):
    code = models.CharField(max_length=100, verbose_name='Course Code')
    capacity = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Exam(models.Model):
    EXAM_TYPES = (
        ('Midterm', 'MIDTERM'),
        ('Final', 'FINAL')
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=EXAM_TYPES, default='Midterm')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'


class TA(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Teaching Assistant'
        verbose_name_plural = 'Teaching Assistants'


class TASchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ta = models.ForeignKey(TA, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TA Schedule'
        verbose_name_plural = 'TA Schedules'


class TAExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, verbose_name='TA')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Exam - TA Schedule'
        verbose_name_plural = 'Exam - TA Schedules'


class TACourse(models.Model):
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, verbose_name='TA')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Master TA'
        verbose_name_plural = 'Master TAs'
