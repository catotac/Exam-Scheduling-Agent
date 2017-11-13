from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Building(models.Model):
    name = models.CharField(max_length=100)
    coord_x = models.FloatField(default=0.0)
    coord_y = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Building'
        verbose_name_plural = 'Buildings'


class Exam(models.Model):
    EXAM_TYPES = (
        ('Midterm', 'MIDTERM'),
        ('Final', 'FINAL')
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=EXAM_TYPES, default='Midterm')
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'


class Classroom(models.Model):
    name = models.CharField(max_length=100, default='Classroom')
    capacity = models.IntegerField()
    max_ta = models.PositiveIntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'


class ClassroomSchedule(models.Model):
    timeslot = models.DateTimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Classroom Busy TimeSlot'
        verbose_name_plural = 'Classroom Busy TimeSlots'


class TA(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Teaching Assistant'
        verbose_name_plural = 'Teaching Assistants'


class TASchedule(models.Model):
    timeslot = models.DateTimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TA Busy TimeSlot'
        verbose_name_plural = 'TA Busy TimeSlots'
