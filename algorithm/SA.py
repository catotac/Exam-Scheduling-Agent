from scheduler import models

import random
import copy
import math


def run_algorithm(initial_temp, nper):
    mid_solution = simulated_annealing('MIDTERM', initial_temp)
    final_solution = simulated_annealing('FINAL', initial_temp)
    print('for midle term: '), print(mid_solution[0])
    print('for final term: '), print(final_solution[0])
    # print(len(mid_solution[1]))
    # print(len(final_solution[1]))
    # print(len(mid_solution[2]))
    # print(len(final_solution[2]))
    solution = {}
    for i in mid_solution[1]:
        value = mid_solution[1].get(i)
        solution[i] = value

    for i in final_solution[1]:
        value = final_solution[1].get(i)
        solution[i] = value
    print(len(solution))

    dic = {}

    for i in mid_solution[2]:
        value = mid_solution[2].get(i)
        dic[i] = value

    for i in final_solution[2]:
        value = final_solution[2].get(i)
        dic[i] = value
    # print(len(dic))
    update_database(solution, dic)
    pass


def simulated_annealing(exam_type, initial_temperature):
    # initial temperature
    temperature = initial_temperature
    temperature0 = temperature

    # fixed nper
    nper = 3

    exam_schedule = models.TAExam.objects.all()
    midterm_dic = {}
    for es_entry in exam_schedule:
        if(es_entry.exam.type == exam_type):
            exist = es_entry.exam in midterm_dic.keys()
            if(exist):
                temp_entry = midterm_dic.get(es_entry.exam)
                temp_entry.append(es_entry)
            else:
                temp_list = []
                temp_list.append(es_entry)
                midterm_dic[es_entry.exam] = temp_list

    #print
    # print('------ check mideterm ---------')
    # for mt_entry in midterm_dic:
    #     print(mt_entry.course.code)
    #     entry = midterm_dic.get(mt_entry)
    #     for i in entry:
    #         print(' ' + i.exam.course.code)


    potential_neighbor = neighbor_relation(midterm_dic)
    neighbor = potential_neighbor[0]

    # print
    # print('------ neighbor relationship -------')
    # print(neighbor)

    # for key_i in neighbor:
    #     value_i = neighbor.get(key_i)
    #     for value in value_i:
    #         print(key_i.course.code + ',' + value.course.code + ' are neighborhoods'),


    index_dic = potential_neighbor[1]
    neighbor_copy = copy.deepcopy(neighbor)

    # convert to current solution list
    # initial solution
    current_solution = {}
    for mt_entry in midterm_dic:
        entry = midterm_dic.get(mt_entry)
        existed_classroom = {}
        classroom_list = []
        current_solution[mt_entry] = classroom_list
        for entry_i in entry:
            classroom = entry_i.classroom
            existc = classroom in existed_classroom.keys()
            if(existc):
                continue
            else:
                existed_classroom[classroom] = 1
                current_solution[mt_entry].append(entry_i.classroom)

    # print('---- check current solution ----')
    # for i in current_solution:
    #     print(i.course.code),
    #     for j in current_solution.get(i):
    #         print(' ' + j.name),


    new_solution = copy.deepcopy(current_solution)
    final_solution = copy.deepcopy(current_solution)

    while(len(neighbor_copy) > 0 and temperature > 1):
        step_count = 1
        while(step_count <= nper):
            cost_old = sa_cost_function(new_solution, midterm_dic)
            if(len(neighbor_copy) == 0):
                break
            random_number = random.randint(1, len(neighbor_copy))
            index_list = random.sample(range(1, len(neighbor_copy) + 1), random_number)

            # print
            # print('----- check index list -------')
            # print(index_list)

            new_result = generate_neighbor_solution(index_dic, index_list, new_solution, neighbor_copy)
            new_solution_after = new_result[0]
            cost_new = sa_cost_function(new_solution_after, midterm_dic)

            sigma = cost_new - cost_old
            check_exp = math.pow(math.e, - sigma/temperature) < random.uniform(0,1)
            if((sigma <= 0) or check_exp):
                new_solution = new_solution_after
                neighbor_copy = new_result[1]
                index_dic = new_result[2]
                new_index_dic = {}
                new_index_dic_counter = 1
                for index_dic_entry in index_dic:
                    element = index_dic[index_dic_entry]
                    new_index_dic[new_index_dic_counter] = element
                    new_index_dic_counter = new_index_dic_counter + 1
                index_dic = copy.deepcopy(new_index_dic)

                # check if the new solution is not valid because of the usage of the same classroom at the same time
                count = 1
                duplicate = False
                for i in new_solution:
                    start_time = i.start_time
                    existed_classroom = {}
                    for j in new_solution.get(i):
                        existed_classroom[j] = 1

                    count_p = 1
                    for i_p in new_solution:
                        if (count_p <= count):
                            count_p = count_p + 1
                            continue
                        start_time_p = i_p.start_time
                        if (start_time == start_time_p):
                            for j_p in new_solution.get(i_p):
                                if (j_p in existed_classroom.keys()):
                                    duplicate = True
                                    break
                            if(duplicate):
                                break
                        count_p = count_p + 1
                    if(duplicate):
                        break
                    count = count + 1
                if(duplicate == False):
                    final_solution = new_solution_after

             # print
            # print('---- check new solution ----')
            # for i in new_solution:
            #     print(i.course.code),
            #     for j in new_solution.get(i):
            #         print(' ' + j.name),
            # print('---- check new neighbor ----')
            # for key_i in neighbor_copy:
            #     value_i = neighbor_copy.get(key_i)
            #     for value in value_i:
            #         print(key_i.course.code + ',' + value.course.code + ' are neighborhoods'),

            # print('---- compare costs -----')
            # print('old cost: '), print(cost_old)
            # print('new cost: '), print(cost_new)

            step_count = step_count + 1

        # print('--- tempperature ----')
        # print(temperature)
        # print(math.log(temperature0))
        # print(math.log(100))
        alpha = 1 - (math.log(temperature0) - math.log(100)) / nper
        temperature = alpha * temperature
        # print(temperature)
        step_count = 1

    # print('---- check current solution ----')
    # for i in current_solution:
    #     print('start time: '), print((i.start_time))
    #     print(i.course.code),
    #     for j in current_solution.get(i):
    #         print(' ' + j.name),
    #
    # print('---- check final solution ----')
    # for i in final_solution:
    #     print('start time: '), print((i.start_time))
    #     print(i.course.code),
    #     for j in final_solution.get(i):
    #         print(' ' + j.name)

    initial_cost = sa_cost_function(current_solution, midterm_dic)
    final_cost = sa_cost_function(final_solution, midterm_dic)

    # print(initial_cost), print(' is the initial cost')
    # print(final_cost), print(' is the final cost')

    final_result = []
    final_result.append(final_cost)
    final_result.append(final_solution)
    final_result.append(midterm_dic)
    return final_result


def neighbor_relation(exam_dic):
    # compute valid neighbors for each exam

        # print(mt_entry.start_time)
        # print(mt_entry.end_time)
        # print(start_time)
        # print(end_time)
        # print(start_time.strftime('%Y-%m-%d'))
        # print(end_time - start_time)
        # print('---------------')

    multi_session = {}
    for mt_entry_i in exam_dic:
        value_i = exam_dic.get(mt_entry_i)
        if (len(value_i) > 1):
            classroom_i = value_i[0].classroom
            multiple_session = False
            for value_entry_i in value_i[1:]:
                if (classroom_i != value_entry_i.classroom):
                    multiple_session = True
            if (multiple_session):
                multi_session[mt_entry_i] = 1

    # print
    # print("----- multiple session ------")
    # for ms_entry in multi_session:
    #     print(ms_entry.course.code)
    # print("----- end ------")


    neighbor = {}
    duplicate_pair = {}
    index_dic = {}

    index_count = 1
    for mt_entry_i in exam_dic:
        if (mt_entry_i in multi_session.keys()):
            continue

        # handle the single assignment case
        exam_date_i = (mt_entry_i.start_time).strftime('%Y-%m-%d')

        for mt_entry_j in exam_dic:
            if (mt_entry_j in multi_session.keys()):
                continue
            if (mt_entry_i != mt_entry_j):
                exam_date_j = (mt_entry_j.start_time).strftime('%Y-%m-%d')
                # check if two exams are held in the same day
                if (exam_date_i == exam_date_j):
                    # check if exam_j is the neighbor of exam_i
                    exam_start_time_i = mt_entry_i.start_time
                    exam_end_time_i = mt_entry_i.end_time
                    exam_start_time_j = mt_entry_j.start_time
                    exam_end_time_j = mt_entry_j.end_time
                    time_duration_i = mt_entry_i.start_time - mt_entry_i.end_time
                    time_duration_j = mt_entry_j.start_time - mt_entry_j.end_time
                    if (time_duration_i == time_duration_j and (
                            exam_end_time_j <= exam_start_time_i or exam_end_time_i <= exam_start_time_j)):
                        # these two exams have the same time duration
                        # then check if these two exams have valid capacities
                        # print(mt_entry_i.course.code + ' ' + exam_dic.get(mt_entry_i)[0].classroom.name)
                        # print(' ' + mt_entry_j.course.code + ' ' + exam_dic.get(mt_entry_j)[0].classroom.name)
                        # print('are potential to be switched')
                        classroom_capacity_i = exam_dic.get(mt_entry_i)[0].classroom.capacity
                        classroom_capacity_j = exam_dic.get(mt_entry_j)[0].classroom.capacity
                        exam_capacity_i = mt_entry_i.course.capacity
                        exam_capacity_j = mt_entry_j.course.capacity
                        if ((classroom_capacity_i >= exam_capacity_j) and (classroom_capacity_j >= exam_capacity_i)):
                            # print(mt_entry_i.course.code)
                            # print(' ' + mt_entry_j.course.code)
                            # print('can be switched')

                            # when both of the switches hold true
                            # print('----- i came here ------')
                            exist = mt_entry_i in neighbor.keys()
                            exam_i = mt_entry_i.course.code
                            exam_j = mt_entry_j.course.code
                            if(exam_i > exam_j):
                                temp_str = exam_i
                                exam_i = exam_j
                                exam_j = temp_str
                            exam_str = exam_i + ',' + exam_j
                            if (exist):
                                duplicate = exam_str in duplicate_pair.keys()
                                if(duplicate == False):
                                    value_i = neighbor.get(mt_entry_i)
                                    value_i.append(mt_entry_j)
                                    duplicate_pair[exam_str] = 1
                            else:
                                duplicate = exam_str in duplicate_pair.keys()
                                if (duplicate == False):
                                    temp_list = []
                                    temp_list.append(mt_entry_j)
                                    neighbor[mt_entry_i] = temp_list
                                    duplicate_pair[exam_str] = 1
                                    index_dic[index_count] = mt_entry_i
                                    index_count = index_count + 1
                    else:
                        continue
                else:
                    # if these two exams are from different dates
                    exam_start_time_i = mt_entry_i.start_time
                    exam_end_time_i = mt_entry_i.end_time
                    exam_start_time_j = mt_entry_j.start_time
                    exam_end_time_j = mt_entry_j.end_time
                    time_duration_i = exam_end_time_i - exam_start_time_i
                    time_duration_j = exam_end_time_j - exam_start_time_j
                    if(time_duration_i == time_duration_j):
                        # these two exams have the same time duration
                        # then check if these two exams have valid capacities
                        # print(mt_entry_i.course.code + ' ' + exam_dic.get(mt_entry_i)[0].classroom.name)
                        # print(' ' + mt_entry_j.course.code + ' ' + exam_dic.get(mt_entry_j)[0].classroom.name)
                        # print('are potential to be switched')
                        classroom_capacity_i = exam_dic.get(mt_entry_i)[0].classroom.capacity
                        classroom_capacity_j = exam_dic.get(mt_entry_j)[0].classroom.capacity
                        exam_capacity_i = mt_entry_i.course.capacity
                        exam_capacity_j = mt_entry_j.course.capacity
                        if ((classroom_capacity_i >= exam_capacity_j) and (classroom_capacity_j >= exam_capacity_i)):
                            # print(mt_entry_i.course.code)
                            # print(' ' + mt_entry_j.course.code)
                            # print('can be switched')

                            # when both of the switches hold true
                            # print('----- i came here ------')
                            exist = mt_entry_i in neighbor.keys()
                            exam_i = mt_entry_i.course.code
                            exam_j = mt_entry_j.course.code
                            if (exam_i > exam_j):
                                temp_str = exam_i
                                exam_i = exam_j
                                exam_j = temp_str
                            exam_str = exam_i + ',' + exam_j
                            if (exist):
                                duplicate = exam_str in duplicate_pair.keys()
                                if (duplicate == False):
                                    value_i = neighbor.get(mt_entry_i)
                                    value_i.append(mt_entry_j)
                                    duplicate_pair[exam_str] = 1
                            else:
                                duplicate = exam_str in duplicate_pair.keys()
                                if (duplicate == False):
                                    temp_list = []
                                    temp_list.append(mt_entry_j)
                                    neighbor[mt_entry_i] = temp_list
                                    duplicate_pair[exam_str] = 1
                                    index_dic[index_count] = mt_entry_i
                                    index_count = index_count + 1
                    else:
                        continue


    result = []
    result.append(neighbor)
    result.append(index_dic)
    return result

def sa_cost_function(solution, exam_dic):
    cost = 0
    for exam_entry in solution:
        # compute distance between TA and exam classroom
        ta_exam = exam_dic.get(exam_entry)
        classroom = solution.get(exam_entry)
        ta_dist = 0
        if(len(classroom) > 1):
            for room in classroom:
                classroom_x = room.building.coord_x
                classroom_y = room.building.coord_y
                for ta in ta_exam:
                    if(ta.classroom.building.name == room.building.name):
                        ta_x = ta.ta.building.coord_x
                        ta_y = ta.ta.building.coord_y
                        dist = math.sqrt(pow(ta_x - classroom_x,2) + pow(ta_y - classroom_y, 2))
                        ta_dist = ta_dist + dist
                        # print(ta_dist)
        else:
            classroom_x = classroom[0].building.coord_x
            classroom_y = classroom[0].building.coord_y
            for ta in ta_exam:
                if (ta.classroom.building.name == classroom[0].building.name):
                    ta_x = ta.ta.building.coord_x
                    ta_y = ta.ta.building.coord_y
                    dist = math.sqrt(pow(ta_x - classroom_x, 2) + pow(ta_y - classroom_y, 2))
                    ta_dist = ta_dist + dist

        # compute distance between exam and course building
        exam_course_dist = 0
        for room in classroom:
            classroom_x = room.building.coord_x
            classroom_y = room.building.coord_y
            course_x = exam_entry.course.building.coord_x
            course_y = exam_entry.course.building.coord_y
            exam_course_dist = exam_course_dist + math.sqrt(pow(course_x - classroom_x, 2) + pow(course_y - classroom_y, 2))

        # compute penalty of capacity
        capacity_of_exam = exam_entry.course.capacity
        capacity_of_classroom = 0
        classroom_list = solution.get(exam_entry)
        for room in classroom_list:
            capacity_of_classroom = capacity_of_classroom + room.capacity
        penalty_capacity = capacity_of_classroom - capacity_of_exam

        cost = cost + ta_dist + 0.1 * exam_course_dist + 0.01 * penalty_capacity
    return cost

def generate_neighbor_solution(index_dic, index_list, current_solution, neighbor):
    neighbor_copy = copy.deepcopy(neighbor)
    new_solution = copy.deepcopy(current_solution)
    index_dic_copy = copy.deepcopy(index_dic)
    exam_date = {}
    for index in index_list:
        exam_i = index_dic_copy.get(index)
        if(neighbor_copy.get(exam_i) == None):
            continue
        exam_j = neighbor_copy.get(exam_i)[0]
        exam_date_i_exist = exam_i in exam_date
        exam_date_j_exist = exam_j in exam_date
        if(exam_date_i_exist):
            date_i_exist = exam_date.get(exam_i)
            current_date_i = (exam_i.start_time).strftime('%Y-%m-%d')
            if(date_i_exist == current_date_i):
                continue

        if(exam_date_j_exist):
            date_j_exist = exam_date.get(exam_j)
            current_date_j = (exam_j.start_time).strftime('%Y-%m-%d')
            if (date_j_exist == current_date_j):
                continue
        exam_date[exam_i] = (exam_i.start_time).strftime('%Y-%m-%d')
        exam_date[exam_j] = (exam_j.start_time).strftime('%Y-%m-%d')
        del neighbor_copy[exam_i][0]
        if(len(neighbor_copy.get(exam_i)) == 0):
            del neighbor_copy[exam_i]
            del index_dic_copy[index]
        classroom_i = new_solution.get(exam_i)
        classroom_j = new_solution.get(exam_j)
        new_solution[exam_i] = classroom_j
        new_solution[exam_j] = classroom_i

    new_index_dic = copy.deepcopy(index_dic_copy)

    # print('---- check final solution ----')
    # for i in new_solution:
    #     print('start time: '), print((i.start_time))
    #     print(i.course.code),
    #     for j in new_solution.get(i):
    #         print(' ' + j.name)
    result_list = []
    result_list.append(new_solution)
    result_list.append(neighbor_copy)
    result_list.append(new_index_dic)
    result_list.append(True)
    return result_list


def update_database(final_solution, exam_dic):
    models.TAExam.objects.all().delete()
    for i in final_solution:
        value = final_solution.get(i)
        if(len(value) > 1):
            for j in exam_dic.get(i):
                database = models.TAExam()
                database.classroom_id = j.classroom.id
                database.exam_id = i.id
                database.ta_id = j.ta.id
                database.save()
        else:
            for j in exam_dic.get(i):
                database = models.TAExam()
                database.classroom_id = value[0].id
                database.exam_id = i.id
                database.ta_id = j.ta.id
                database.save()
    pass