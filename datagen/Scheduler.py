import random
from datetime import datetime, timedelta
from pytz import timezone
import coms572_final.settings as settings


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
                        'building_id': random.randint(0, len(self._building_list)-1)}
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
                        'building_id': random.randint(0, len(self._building_list)-1)}
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
                        'email': 'ta_email' + str(random.randint(10, 99)) + '@test.com',
                        'building_id': random.randint(0, len(self._building_list)-1)}
                retlist.append(temp)

        return retlist


class ScheduleGenerator(object):

    def __init__(self, num_parents=5, num_instances=2, min_date=None, max_date=None, min_duration=60, max_duration=180):
        self._num_parents = num_parents
        self._num_instances = num_instances
        self._min_date = min_date
        self._max_date = max_date
        self._min_duration = min_duration
        self._max_duration = max_duration

    def generate(self, min_time=datetime.now(timezone(settings.TIME_ZONE)), max_time=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(hours=8)):
        retlist = []

        if self._min_date and self._max_date:
            counter = 0
            for parent_id in range(0, self._num_parents):
                for num in range(0, self._num_instances):
                    d = self._random_date()
                    ti = random.randint(int(min_time.timestamp()), int(max_time.timestamp()))
                    t = datetime.fromtimestamp(ti)
                    start_date = datetime(year=d.year, month=d.month, day=d.day)
                    start_date = start_date.replace(hour=t.hour, minute=t.minute, second=t.second, tzinfo=timezone(settings.TIME_ZONE))
                    temp = {'id': counter,
                            'start_time': start_date,
                            'end_time': start_date + timedelta(minutes=random.randint(self._min_duration, self._max_duration)),
                            'parent_id': parent_id}
                    retlist.append(temp)
                    counter += 1

        return retlist

    # Inspired from https://stackoverflow.com/a/81706518
    def _random_date(self):
        return self._min_date + timedelta(
            minutes=random.randint(0, int((self._max_date - self._min_date).total_seconds() / 60)-1),
        )
