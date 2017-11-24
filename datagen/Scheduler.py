import random
import datetime


class BuildingGenerator(object):

    def __init__(self, num_instances=5, coord_start=-10.0, coord_end=10.0):
        self._generic_name = 'Building'
        self._num_instances = num_instances
        self._coord_start = coord_start
        self._coord_end = coord_end

    def generate(self):
        retlist = []

        for num in range(0, self._num_instances):
            temp = {'id': num,
                    'name': self._generic_name + str(num),
                    'coord_x': random.uniform(self._coord_start, self._coord_end),
                    'coord_y': random.uniform(self._coord_start, self._coord_end)}
            retlist.append(temp)

        return retlist


class ClassroomGenerator(object):

    def __init__(self, buildings=None, num_instances=5, min_capacity=25, max_capacity=250, max_ta=3):
        self._generic_name = 'Classroom'
        self._num_instances = num_instances
        self._min_capacity = min_capacity
        self._max_capacity = max_capacity
        self._max_ta = max_ta
        self._building_list = buildings

    def generate(self):
        retlist = []

        if self._min_capacity > self._max_capacity:
            return retlist

        if self._building_list:
            for num in range(0, self._num_instances):
                temp = {'id': num,
                        'name': self._generic_name + str(num),
                        'capacity': random.randint(self._min_capacity, self._max_capacity),
                        'max_ta': random.randint(1, self._max_ta),
                        'building_id': random.randint(0, len(self._building_list))}
                retlist.append(temp)

        return retlist


class CourseGenerator(object):

    def __init__(self, buildings=None, num_instances=10, min_capacity=35, max_capacity=500):
        self._generic_name = 'Course'
        self._num_instances = num_instances
        self._min_capacity = min_capacity
        self._max_capacity = max_capacity
        self._building_list = buildings

    def generate(self):
        retlist = []

        if self._min_capacity > self._max_capacity:
            return retlist

        if self._building_list:
            for num in range(0, self._num_instances):
                temp = {'id': num,
                        'code': self._generic_name + ' ' + str(random.randint(1, 6)) + '0' + str(num),
                        'capacity': random.randint(self._min_capacity, self._max_capacity),
                        'building_id': random.randint(0, len(self._building_list))}
                retlist.append(temp)

        return retlist


class TAGenerator(object):

    def __init__(self, buildings=None, num_instances=5):
        self._generic_first_name = 'John'
        self._generic_last_name = 'Doe'
        self._num_instances = num_instances
        self._building_list = buildings

    def generate(self):
        retlist = []

        if self._building_list:
            for num in range(0, self._num_instances):
                temp = {'id': num,
                        'first_name': self._generic_first_name + str(random.randint(100, 999)),
                        'last_name': self._generic_last_name + str(random.randint(100, 999)),
                        'building_id': random.randint(0, len(self._building_list))}
                retlist.append(temp)

        return retlist


class ScheduleGenerator(object):

    def __init__(self, num_instances=2, min_time=None, max_time=None, min_duration=60, max_duration=180):
        self._num_instances = num_instances
        self._min_time = min_time
        self._max_time = max_time
        self._min_duration = min_duration
        self._max_duration = max_duration

    def generate(self, obj_id):
        retlist = []

        if self._min_time and self._max_time:
            for num in range(0, self._num_instances):
                start_time = self._random_date()
                temp = [start_time,
                        start_time + datetime.timedelta(minutes=random.randint(self._min_duration, self._max_duration)),
                        obj_id]
                retlist.append(temp)

        return retlist

    # Inspired from https://stackoverflow.com/a/81706518
    def _random_date(self):
        return self._min_time + datetime.timedelta(
            minutes=random.randint(0, int((self._max_time - self._min_time).total_minutes())),
        )