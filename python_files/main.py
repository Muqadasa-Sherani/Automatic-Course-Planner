import csv

import sys
sys.path.append(".")

from objects import *  # import all classes in objects.py


department_courses = []  # list of all department courses
service_courses = []  # list of all service courses
instructor_list = []  # list of all instructors with their busy times


# time formats: 
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
times = ["Morning", "Afternoon"]

def find(liste, name):  # boolean
    for obj in liste:
        if str(obj) == name:
            return True
    else:
        return False

def find_obj(liste, name):  # returns found object
    for obj in liste:
        if str(obj) == name:
            return obj
            

# take courses. separate them into 2 groups: D and S
# please change it's extension for your case. my csv tables are in desktop. I used ../ because of that.
with open('tables/Courses.csv') as csv_file:  # WARNING: different IDEs require different paths. We used VScode for this project, thus this path.
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    for row in csv_reader:
        if find(instructor_list, row[6]) == False:  # no duplicate instructor
            inst = Instructor(row[6])
            instructor_list.append(inst)
        else:
            inst = find_obj(instructor_list, row[6])
        if row[5] == "D":  # department course
            department_courses.append(Course(row[0], row[1], row[2], row[3], row[4], row[5], inst))
        else:  # service course
            service_courses.append(Course(row[0], row[1], row[2], row[3], row[4], row[5], inst))

# take busy time
with open('tables/busy.csv') as csv_file:  # WARNING: different IDEs require different paths. We used VScode for this project, thus this path.
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:  
        if find(instructor_list, row[0]):  # if there is instructor with that name
            find_obj(instructor_list, row[0]).setBusyTime(row[1], row[2]) 

bigRoom = 0  # number of big rooms
smallRoom = 0  # number of small rooms

with open('tables/classroom.csv') as csv_file:  # WARNING: different IDEs require different paths. We used VScode for this project, thus this path.
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:  
        if row[0] == "big":
            bigRoom = int(row[1])
        elif row[0] == "small":    
            smallRoom = int(row[1])


schedule = Schedule(bigRoom, smallRoom)  # new instance of a schedule
    
with open('tables/service.csv') as csv_file:  # WARNING: different IDEs require different paths. We used VScode for this project, thus this path.
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:  
        s_course = find_obj(service_courses, row[0])  # finding service course by its id
        if schedule.hasBigRoom(row[1], row[2]) and (s_course._compulsary_elective == "C" or not(schedule.hasSmallRoom(row[1], row[2]))):  # compulsory or there is no room for elective
            schedule.addToSchedule(row[0], "bigRoom", row[1], row[2])  # code, room, day, time
            s_course.setRoom()  # set hasRoom == True
            
        elif(schedule.hasSmallRoom(row[1], row[2])):
            schedule.addToSchedule(row[0], "smallRoom", row[1], row[2])  # code, room, day, time
            s_course.setRoom()  # set hasRoom == True

all_courses = department_courses + service_courses  # all courses
def hasSameYear(schedule, year):
    for s in schedule:
        course = find_obj(all_courses, s._code)
        if course._year == year:        
            return True
    return False

def makeSchedule(schedule, d_list):
    # department courses will be added to schedule according to the defined constraints 
    for d_c in d_list:
        for day in days:
            for time in times:
                if d_c._hasRoom or d_c._instructor.isBusy(day, time):  # if the course has already been assigned a room or intructor is busy at that time
                    break 
                elif not hasSameYear(schedule.schedule_table[day][time], d_c._year):  # if the course already present in that time slot is not the same as the one we are about to insert
                    if schedule.hasBigRoom(day, time) and (d_c._compulsary_elective == "C" or not(schedule.hasSmallRoom(day, time))):
                        schedule.addToSchedule(d_c._code, "bigRoom", day, time)  # code, room, day, time
                        d_c.setRoom()  # set hasRoom == True
                    elif d_c._compulsary_elective == "E" and schedule.hasSmallRoom(day, time):
                        schedule.addToSchedule(d_c._code, "smallRoom", day, time)  # code, room, day, time
                        d_c.setRoom()  # set hasRoom == True
                    


def anyCourseLeft(d_list, stack_left): # lists any course that has not been placed in schedule
    flag = True
    for d in d_list:
        if not d._hasRoom:
            stack_left.append(d)
            flag = False  # flag become false if there any left over course
    return flag

# we are going to swap some time slots with the left-over courses
def placeLeftCourses(schedule, stack_left, stack_replaced):
    flag2 = True
    for c in stack_left:
        flag2 = True
        for day in days:
            for time in times:  
                for i in range(schedule[day][time].__len__()):
                    if not hasSameYear(schedule[day][time], c._year) and not find(service_courses, schedule[day][time][i]._code):
                        course = find_obj(department_courses, schedule[day][time][i]._code)  # find department course
                        course.setEmpty()  # remove the current course from schedule
                        schedule[day][time][i].replace(c._code)  # replace the course with one of the left-over courses
                        c.setRoom()
                        stack_replaced.append(course)  # put the removed course back to stack
                        flag2 = False
                    if not flag2:
                        break

stack_left = []  # courses left over
stack_replaced = []  # courses will be replaced with left-over courses

makeSchedule(schedule, department_courses)
flag = anyCourseLeft(department_courses, stack_left)  # if there is left over courses flag is false, left courses will be printed -> schedule is not completed

if not flag:  # there are courses that don't have any room
    placeLeftCourses(schedule.schedule_table, stack_left, stack_replaced)  # place these courses to available place
    makeSchedule(schedule, stack_replaced)  # place replaced courses to schedule
    flag = anyCourseLeft(department_courses, stack_left)  # if flag is true, there is a schedule
    if flag:
        print("\nThere is a schedule: \n") 
        schedule.display()
    else:  # if flag is false, no schedule is produced for courses
        print("There is no way to make a schedule for the department.")   

else:  # if flag is true, there is a schedule
    print("\n*There is a schedule: \n") 
    schedule.display()


