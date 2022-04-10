class Course:

    def __init__(self, code, name, year, credit, compulsary_elective, department_service, instructor):

        self._code = code
        self._name = name
        self._year = year
        self._credit = credit
        self._compulsary_elective = compulsary_elective
        self._department_service = department_service
        self._instructor = instructor
        self._hasRoom = False # initially a course has not room
        
    def setRoom(self):
        self._hasRoom = True # this course is placed 

    def setEmpty(self):
        self._hasRoom = False 
        
    def __str__(self):
        return self._code

class Instructor:
    def __init__(self, name):
        self._name = name
        self._busy_time = []

    def setBusyTime (self,day,time) :  self._busy_time.append(BusyTime(day,time))

    def isBusy (self, day, time): 
        for b in self._busy_time:
            if b._day == day and b._time == time:
                return True
        return False

    def __str__(self):
        return self._name


# instructors may have more than one busy time. time format: 

class BusyTime:
    def __init__(self, day, time):
        self._day = day
        self._time = time

class Schedule:
    
    def __init__(self, bigRoom, smallRoom):
        self.schedule_table = {"Monday": {"Morning": [], "Afternoon": []}, "Tuesday": {"Morning": [], "Afternoon": []}, 
                        "Wednesday": {"Morning": [], "Afternoon": []}, "Thursday":{"Morning": [], "Afternoon": []}, 
                        "Friday": {"Morning": [], "Afternoon": []}}

        self._bigRoom = bigRoom # number of bigRooms
        self._smallRoom = smallRoom # number of smallRooms

        # number of used rooms for each time slot
        # exp: used_bigRooms[Morning][Afternoon] = 2 ->> means 2 big class is used in schedule for that time slot
        # set initally 0 all of them, increase when a course is added into schedule_table

        self.used_bigRooms = {"Monday": {"Morning": 0, "Afternoon": 0}, "Tuesday": {"Morning": 0, "Afternoon": 0}, 
            "Wednesday": {"Morning": 0, "Afternoon": 0}, "Thursday":{"Morning": 0, "Afternoon": 0}, "Friday": {"Morning": 0, "Afternoon": 0}}
        self.used_smallRooms = {"Monday": {"Morning": 0, "Afternoon": 0}, "Tuesday": {"Morning": 0, "Afternoon": 0}, 
            "Wednesday": {"Morning": 0, "Afternoon": 0}, "Thursday":{"Morning": 0, "Afternoon": 0}, "Friday": {"Morning": 0, "Afternoon": 0}}  
        
    def hasBigRoom(self, day, time): # checks availability of bigRooms
        if self.used_bigRooms[day][time] < self._bigRoom:
            return True
        return False

    def hasSmallRoom(self, day, time): # checks availability of smallRooms
        if self.used_smallRooms[day][time] < self._smallRoom:
            return True
        return False
 
    def addToSchedule(self, code, roomSize,  day, time):
        if roomSize == "bigRoom":
            self.used_bigRooms[day][time] += 1
            room = (roomSize + str (self.used_bigRooms[day][time]))
        else:
            self.used_smallRooms[day][time] += 1
            room = (roomSize + str (self.used_smallRooms[day][time]))
        self.schedule_table[day][time].append(ScheduleFormat(code, room, day, time))
    
    def display(self):

        days = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday"]

        for day in days:
            for s in self.schedule_table[day]["Morning"]:
                s.display()
            for s in self.schedule_table[day]["Afternoon"]:
                s.display()

            print("****************************************")

# exp: Math 101, bigRoom3, Friday, Morning

class ScheduleFormat:
    def __init__(self, code, room, day, time):

        self._day = day # day and time
        self._time = time
        self._code = code # course code
        self._room = room # big or small with index 

    def display(self):
        print(self._day + " " + self._time + " " + self._room + " " + self._code)


    def replace(self, code):
        self._code = code

