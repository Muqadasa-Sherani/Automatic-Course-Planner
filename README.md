# Automatic-Course-Planner
This is my second year project. In this project, we implemented an automatic course planner for a curriculum semester of a department. 
In the curriculum, there are several courses for each year of the curriculum. 
The program assigns a classroom and a time slot for each course in the curriculum. 
Courses in the same year are not intersected with each other (i.e., see CENG Spring curriculum). 
There is some intersection between courses of different years. 
There are 2 different types of the classroom: big and small. 
Mandatory courses in the curriculum should be assigned to a big classroom. Elective courses can be assigned to a big or small classroom according to the availability of them. 
There is a limited number of dedicated classrooms for the department. 
The number of each type of classroom should be read from an excel file. 
Besides, for each weekday there are 2-time slots available, morning and afternoon. 
So, there are in total 10 time slots available to place a course (5 weekdays*2 time slot).
In the department curriculum, there are some service courses which are given by another department at the university. 
The time slot of these courses is fixed and predefined. Therefore, we cannot assign different time slots for those courses other than the requested time slot. 
Furthermore, some instructors may not be available for some time slots. Thus, the program respect these busy time slots for the respective courses. 
All these constraints are taken from an excel file. We haven't assumed anything in prior and we haven't used any hard-coded parameter / value in our code.
In the end, the program prints the course schedule for the department. 
In this schedule, there is no intersection between courses for a year of the curriculum and ther is respect to all constraints. 
If the program cannot find any possible schedule it prints a message “There is no way to make a schedule for the department.”

Note:
- There is a pseudocode pdf file in the repository.
- we used GUI to take information from the students.
