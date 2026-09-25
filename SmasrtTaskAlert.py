import json
from datetime import datetime


FILE_NAME = "smart_task_alert_data.json"

STATUS_OPTIONS = [
    "Pending",
    "Processing",
    "Completed"
]

categories = [
    "title",
    "subject",
    "due date",
    "status"
]

# ==============
# borders 
# ==============
errors = f"\n{'x' * 50}"
sub = f"\n{'-' * 58}"
double = f"\n{'=' * 50}"



# ============================================================
# FILE HANDLING
# ============================================================
#  this function is the default data structure ng jsonfile
def create_default_data():
# if wala pang data or usa na data, ito yung gagamitin nya since yung default
    return {
# dto yung information ni student
        "student": {
            "name": "",
            "course": ""
        },
# tapos dto i-store or hold yung mga subjects data
        "subjects": [],
# dto nmn yung task na na-enter ng user
        "tasks": []
    }

# this function is nag rread ng mga exixting data sa jsonfile ntin
def load_data():
# gumamit tayo ng try function para ma handle yung possible errors
    try:
        # with function is to open and close the file after reading it
        with open(FILE_NAME, "r") as file:
            # then yung na read na data convert natin as dict then yung data variable ang mag hhold nung dic nayun
            data = json.load(file)

        # isinstance is checking if the data is in a dict format
        if not isinstance(data, dict):
            # if the condition is false mag pprint sya ng mga error sa baba
            print(errors)
            print("Invalid data file. Creating a new one.")
            print(errors)
            # then gagawa sya ng bagong default data
            return create_default_data()

        # check natin kung may student key na
        # kapag wala, then gagawa ulit ng student key
        # gamit yung default name and course
        data.setdefault("student", {
            "name": "",
            "course": ""
        })
        # check the data if may subject and task na then if wala create ng empty list
        data.setdefault("subjects", [])
        data.setdefault("tasks", [])

        # then return the data
        return data

    except FileNotFoundError:
        data = create_default_data()
        save_data(data)
        return data
    # if invalid yung laman ng jsonfile mag shhow ng error message then mag ccreate sya ng bagong data and save it 
    except json.JSONDecodeError:
        print(errors)
        print("Warning: The JSON file is corrupted or invalid.")
        print("Creating a new data file.")
        print(errors)

        data = create_default_data()
        save_data(data)

        return data

# this function is to save yung code natin into json file
def save_data(data):
# try to catch the errors
    try:
        # open the file and 'w' is to write a date then after that the file will automatically close
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)
# catching the operating system error kung hindi nag ssave si file
    except OSError as error:
        print(f"Error saving data: {error}")

# ============================================================
# INITIAL SETUP
# ============================================================
# this function is to set up the information of the user or student before mag run yung main menu
def setup_student(data):
    student = data["student"]

    # If student information already exists,
    # don't ask for it again every time.
    if student["name"] and student["course"] and data["subjects"]:
        return

    print(double)
    print("         STUDENT SETUP")
    print(double)

    while True:
        # ask the user for their name
        name = input("Enter your name: ").strip()
        # pag may value na break the loop
        if name:
            break

        print(errors)
        print("Name cannot be empty.")
        print(errors)

    while True:
        # keep asking the user for the courses until the input is valid
        course = input("Enter your course: ").strip()
        if course:
            break
        print(errors)
        print("Course cannot be empty.")
        print(errors)

    subjects = []
    print("\nEnter your subjects.")
    print("Type 'done' when you are finished.")
    while True:
        # then ask for the next subject then use the subjects list length for subject number
        subject_name = input(f"Enter Subject {len(subjects) + 1}: ").strip()
        # check the value of subject name then validate
        if subject_name.lower() == "done":
            if not subjects:
                print(errors)
                print("You must enter at least one subject.")
                print(errors)
                continue

            break
        # if the value is empty then print error message and continue asking for subject
        if not subject_name:
            print(errors)
            print("Subject cannot be empty.")
            print(errors)
            continue

        duplicate = False #this variable is use for cheking if the subject is alsready exist
        # check for each subject na nasa subjects list
        for subject in subjects:
            if subject["name"].lower() == subject_name.lower():#lowe function is to convert all text in lower case
                duplicate = True #then change the value of duplicate
                break #then break 

        if duplicate: #if duplicate is false then print errors
            print(errors)
            print("That subject already exists.")
            print(errors)
            continue # ask another subject
        #create a dictionary for subjects
        subject = {
            "id": len(subjects) + 1, #id is based sa index ng subject 
            "name": subject_name,
            "details": {}
        }

        subjects.append(subject) # then append the subject dictionary in the subjects list
    # save the input information into the main data
    data["student"]["name"] = name
    data["student"]["course"] = course
    data["subjects"] = subjects
    # save the updated info into json file
    save_data(data)

    print(sub)
    print("\nStudent information saved successfully!")
    print(sub)

# ============================================================
# DASHBOARD
# ============================================================
#this function is to show the main dashboard
def show_dashboard(data):
    """then get the the student info from the main data
        same for subjects and tasks
    """
    student = data["student"]
    subjects = data["subjects"]
    tasks = data["tasks"]
# TITLE
    print("\n========================================")
    print(f"{'SMART TASK ALERT':^30}")
    print(f"{'Digital Assignment Monitoring System':^30}")
    print("========================================")
# GREETINGS FOR STUDENT
    print(f"Welcome, {student['name']}!")
    print(f"Course: {student['course']}")

    print("\n--- TASK STATUS ---")
# TABLE FOR TASKS AND NUMBER STATUS FOR EACH SUBJECTS TASK
    if not subjects: # CHECK FOR SUBJECTS
        print("No subjects found.")
        return

    #TABLE HEADER
    print(f"\n{'ID No.':<10}|{'Subjects':<10}", end="|") # IF SUBJECTS IS IN A SUBJECTS LIST
    for stats in range(len(STATUS_OPTIONS)): # ITERATE THE STATUS OPTION
        print(f"{STATUS_OPTIONS[stats]:<11}", end="|")
    print(f"{sub}")

    for subject in subjects: #FOR EACH SUBJECT IN SUBJECTS LIST 
        subject_id = subject["id"] # CREATE A VARIABLE THAT CONTAINS THE ID OF SUBJECTS

        pending = 0
        processing = 0
        completed = 0

        for task in tasks: # FOR EACH TASK IN TASKS DICTIONARY
            if task["subject_id"] == subject_id: # COMPARE THE ID
                if task["status"] == "Pending": #IF ID IS PENDING
                    pending += 1 #UPDATE STATUS
                elif task["status"] == "Processing":
                    processing += 1
                elif task["status"] == "Completed":
                    completed += 1
        #TABLE ROW
        #ROWS CONTAINS ID, SUBJECT NAME, AND STATUS
        tb_row = f"ID: {subject_id:<6}|{subject['name']:<10}|{pending:^10} | {processing:^9} | {completed:^10}|"
        length_row = len(tb_row)
        border = "-" * length_row
        print(f"\n{tb_row}\n{border}", end="")
    print()

        # print(f"    Processing: {processing}")
        # print(f"    Completed:  {completed}")

# ============================================================
# MAIN MENU
# ============================================================
#THIS FUNCTION PERFORMS THE MAIN MENU OF THE SYSTEM
def main_menu(data):
    #LIST OF FUNCTION 
    menu = [
        "Add New Task",
        "View All Tasks",
        "View all Upcoming Deadlines",
        "Search Assignment",
        "Update Task",
        "Delete Task",
        "Exit"
    ]
    #INFINITELY RUNNING UNTIL THE USER ENTER THE NO."6" TO EXIT THE FUNCTION
    while True:
        #CALL THE DASHBOARD FUNCTION TO SHOW THE DASHBOARD
        show_dashboard(data)
        print("\n========================================")
        print(f"{'MAIN MENU':^40}")
        print("========================================")
        # ITERATE THE MENU LIST
        for index, option in enumerate(menu, 1):
            #SHOW THE INDEX AND THE NAME OF FUNCTION
            print(f"{index}. {option}")
        #TRY TO CATCH AN ERROR IF THE USER ENTERS UNINTENDED INPUT
        try:
            print("=" * 40)
            choice = int(input("PLEASE ENTER AN OPTION HERE : ")) #ASK THE USER TO ENTER THE SELECTED OPTION HERE
        except ValueError:
            print("\nInvalid input. Please enter a number.") #IF THERE'S AN ERROR
            continue # ASK THE USER AGAIN 
        
        """ VALIDATING THE CHOICE TO PERFORM EACH FUNCTION OF SELECTED CHOICE"""
        if choice == 1: 
            add_task(data)
        elif choice == 2:
            view_all_tasks(data)
        elif choice == 3:
            view_all_upcomingDeadlines(data)
        elif choice == 4:
            search_assignment(data)
        elif choice == 5:
            update_task(data)
        elif choice == 6:
            delete_task(data)
        elif choice == 7:
            save_data(data)
            print(sub)
            print("\nThank you for using Smart Task Alert!")
            print(sub)
            break
        else:
            print(errors)
            print("\nInvalid option. Please choose 1 to 6.")
            print(errors)

# ============================================================
# ADD TASK
# ============================================================
#THIS FUNCTION IS TO ADD AN ASSIGNMENT OR TASK
def add_task(data):
    """WHILE LOOP IS TO INFINITE LOOP THE PROGRAM UNTIL THE INTENDED INPUT IS VALIDATED"""
    while True:
        print(double)
        print(f"{'ADD NEW TASK':^40}")
        print(double)
        print("Process:")
        print("1. Enter task information")
        print("2. Select task status")
        print("3. Save the task")
        title = input("\nEnter task title: ").strip()
        if title == "": # IF THE TITLE IS EMPTY PRINT THE ERRORS BELOW
            print(errors)
            print("\nTask title cannot be empty.")
            print(errors)
        else: #ELSE BREAK THE LOOP
            break
    # ----------------------------------------
    # SELECT SUBJECT
    # ----------------------------------------
    selected_subj_list = [] #SELECTED SUBJECT LIST FOR CONSOLIDATING THE DATA FROM MAIN DATA

    print("\nAvailable Subjects:")
    for subject in data["subjects"]: # FOR EACH SUBJECTS NA NASA DATA DICTIONARY GIVE THOSE DATA TO THE SUBJECT VARIABLE
        print(f"[{subject['id']}] {subject['name']}") #THEN PRINT THE SUBJECT ID AND THE SUBJECT NAME
        selected_subj_list.append(subject["name"]) #THEN APPEND THE NAME TO THE SELECTED_SUBJ_LIST

    selected_subject = None # THIS IS FOR CHECKING THE SUBJECT IN THE LIST

    while True:
        try:
            rangeVal = len(selected_subj_list) # GET THE INT VALUE OF THE LIST
            subject_id = int(input("\nEnter Subject ID: ")) #ASK THE USER FOR SUBJECT ID
            if subject_id not in range(rangeVal):# IF THE VALUE IS GREATER THAN OR LESS THAN THE RANGEVAL
                print(errors)
                print(f"Select Option Between (1 - {rangeVal})") # PRINT THIS ERROR MESSAGE
                print(errors)

        except ValueError:
            print(errors)
            print("Invalid Subject ID.") # IF USER ENTER A VALUE THAT IS NOT AN INTEGER THEN SHOW THIS MESSAGE
            print(errors)
            continue # THEN CONTINUE ASKING

        for subject in data["subjects"]: #GET THE SUBJECT DATA FROM THE MAIN DATA
            if subject["id"] == subject_id: #COMPARE THE ID
                selected_subject = subject #THEN GIVE THE VALUE TO SELECTED_SUBJECT VARIABLE
                break #THEN BREAK

        if selected_subject is not None: #IF THE SELECTED_SUBJECT HAS A VALUE 
            break # THEN BREAK THE LOOP
        print(errors)
        print("Subject not found.") # IF SELECTED SUBJECT IS NONE PRINT THIS
        print(errors)

    # ----------------------------------------
    # DATE
    # ----------------------------------------
    while True:
        # 
        due_date = input("Enter due date (MM/DD/YYYY): ").strip()
        try:
            # datetime.strptime() checks whether the text follows the specified date format.
            datetime.strptime(due_date, "%m/%d/%Y")
            break #THEN IF THE VALUE IS VALID, BREAK THE LOOP
        except ValueError:
            print("Invalid date. Example: 09/30/2026")

    # ----------------------------------------
    # TIME
    # ----------------------------------------

    while True:
        due_time = input("Enter due time (HH:MM AM/PM): ").strip()
        try:
            # This checks if the entered time
            datetime.strptime(due_time, "%I:%M %p") 
            break
        except ValueError:
            print(errors)
            print("Invalid time. Example: 10:30 PM")
            print(errors)

    # ----------------------------------------
    # STATUS
    # ----------------------------------------

    print("\nSelect Task Status:")

    for index, status in enumerate(STATUS_OPTIONS, 1): #ITERATE THE STATUS OPTIONS
        print(f"[{index}] {status}") # THEN PRINT THE INDEX AND STATUS
    while True:
        try:
            status_choice = int(input("Enter status number: ")) # ASK FOR INDEX OF STATUS 
            range_val = len(STATUS_OPTIONS) # CONVERTING THE LIST TO INT 
            if status_choice not in range(1, len(STATUS_OPTIONS) + 1): # IF CHOICE IS WALA SA RANGE NG STATUS WHICH IS 1 - 3
                print(f"Enter an Option between [1 - {range_val}].") # IF CONDITION IS TRUE PRINT THIS

        except ValueError:
            print("Invalid status option.")
            continue

        if status_choice in range(range_val): #CHECK THE CHOICE IF THE NASA RANGE 
            break # IF TRUE, BREAK LOOP
            

    selected_status = STATUS_OPTIONS[status_choice - 1] # NAG MINUS TAYO SINCE YUNG INDEXING NG LIST IS NAG START TO "0"
                                                        # DO IF THE SELECTED IS 1 THEN - 1 = 0, SO THE CHOICE CAN ACCESS THE INTENDED INDEX
    # ----------------------------------------
    # CREATE TASK
    # ----------------------------------------

    task = {
        "id": get_next_task_id(data), # TO GET THE SUBJECT ID AND UPDATE
        #THEN ADD THE NEW ASSIGNMENT DETAILS THAT THE USER CREATED
        "subject_id": subject_id,
        "title": title,
        "due_date": due_date,
        "due_time": due_time,
        "status": selected_status
    }

    data["tasks"].append(task) # THEN APPEND TASK DATA TO THE MAIN DATA TASKS
    # ----------------------------------------
    # ADD MORE
    # ----------------------------------------
    #OPTIONAL IF THE USER WANTS TO ADD ANOTHER ASSIGNMENT/TASK
    while True:
        # ASK THE USER TO CHOOSE
            choice = input(f"\n[+] Add another task [C] Cancel / Back to Main Menu\n\nSelect: ").strip().lower()
            if choice == "+": # VALIDATE
                add_task(data) # IF TRUE THEN PERFORM THE FUNCTION AGAIN
                return # THEN RETURN A VALUE
            elif choice == "c": # VALIDATE
                save_data(data) #SAVE THE DATA
                print(double)
                print("\nTask saved successfully!") # SHOW SUCCESSFUL MESSAGE
                print(double)
                return #THEN RETURN TO THE MAIN MENU

            else:
                print(errors)
                print("Invalid option. Enter + or C.")
                print(errors)

# ============================================================
# GET NEXT TASK ID
# ============================================================
# GETTING THE LATEST OR HIGHEST ID FROM THE MAIN DATA TO AVOID REPLICATION OF AN ID
def get_next_task_id(data):
# IF THERE'S NO TASK YET 
    if not data["tasks"]:
        return 1 # SET THE ID AS 1
#CREATE A VARIABLE TO STORE THE HIGHEST ID
    highest_id = 0
#THEN CHECK THE EXISTING DATA TO THE MAIN DATA
    for task in data["tasks"]:
        if task["id"] > highest_id: # COMPARE THE ID 
            highest_id = task["id"] # THEN STORE IT TO THE HIGHEST_ID VARIABLE

    return highest_id + 1 # THEN UPDATE THE VALUE 

# ============================================================
# VIEW ALL TASKS
# ============================================================
# THIS FUNCTINO IS TO VIEW ALL THE LIST TASK IN EACH SUBJECT
def view_all_tasks(data):

    print("\n========================================")
    print(f"{'ALL TASKS':^40}")
    print("========================================")

# CHECK SUBJECT FROM THE MAIN DATA
    if not data["subjects"]: # IF THERE'S NO SUBJECTS FROM THE DATA 
        print("No subjects found.") # PRINT THE MESSAGE
        return # THEN RETURN TO THE MAIN MENU

    for subject in data["subjects"]: # LAHAT NG SUBJECTS NA NASA DATA ILALAGAY NYA KAY SUBJECT VARIABLE

        subject_id = subject["id"] # YUNG MGA ID NA NASA SUBJECT I-STORE NYA KAY SUBJECT-ID
        subject_name = subject["name"] # SAME LAN HERE PERO NAME NMN YUNG INISTORE

        print(f"\n------------------- {subject_name.upper()} ---------------------------------------")

        subject_tasks = []

        for task in data["tasks"]: #KUNIN NMN NATIN YUNG TASKS NA NASA MAIN DATA
            if task["subject_id"] == subject_id: # THEN COMPARE NATIN SA SUBJECT ID
                subject_tasks.append(task) # THEN APPEND NATIN SA SUBJECT_TASK LIST

        if not subject_tasks: # IF SUBJECT LIST IS NONE
            print("No tasks for this subject.") # PRINT THIS 
            continue # THEN CONTINUE THE PROGRAM
        # THEN PRINT THE CODE BELOW
        print(f"{'ID No.':<10}|{'Title':^30}|{'Due Date':^15}|{'Due time':^15}|{'Status':^15}") 
        for task in subject_tasks:
            print(f"ID:{task['id']:<7}|{task['title'].upper():<30}|{task['due_date']:^15}|{task['due_time']:^15}|{task['status']:^15}")

"""            # print(f"\nTask ID: {task['id']}")
            # print(f"Title: {task['title']}")
            # print(f"Due Date: {task['due_date']}")
            # print(f"Due Time: {task['due_time']}")
            # print(f"Status: {task['status']}")"""

# ============================================================
# VIEW ALL TASKS
# ============================================================
def view_all_upcomingDeadlines(data):
    print(double)
    print(f"\nNot Yet Implemented/Created")
    print(f"\nWE ARE WORKING FOR THIS FUNCTION TO BE CREATED")
    print(double)

# ============================================================
# SEARCH ASSIGNMENT
# ============================================================

def search_assignment(data):

    print("\n========================================")
    print("          SEARCH ASSIGNMENT")
    print("========================================")
    # CHACK IF THE MAIN DATA CONTAINS SUBJECTS
    if not data["subjects"]:
        print("No subjects found.")
        return

    print("\nSubjects:")
    # KUNIN YUNG DATA NG SUBJECTS NA NASA MAIN DATA
    for subject in data["subjects"]:
        # THEN PRINT THE ID AND SUBJECT NAME
        print(f"[{subject['id']}] {subject['name']}")

    try:
        subject_id = int(input("\nEnter Subject ID: ")) # ASK THE USER FOR SUBJ ID

    except ValueError:
        print("Invalid Subject ID.") # IF UNINTENDED INPUT IS ENTERED, PRINT THIS
        return # THEN RETURN TO MAIN MENU

    selected_subject = None

    for subject in data["subjects"]:
        if subject["id"] == subject_id:
            selected_subject = subject
            break

    if selected_subject is None:
        print("Subject not found.")
        return

    subject_tasks = []

    for task in data["tasks"]:
        if task["subject_id"] == subject_id:
            subject_tasks.append(task)

    if not subject_tasks:
        print(
            f"\nNo tasks found for "
            f"{selected_subject['name']}."
        )
        return

    print(f"\n--- {selected_subject['name']} ---")

    for task in subject_tasks:
        print(
            f"[{task['id']}] "
            f"{task['title']} - "
            f"{task['status']}"
        )

    try:
        task_id = int(
            input("\nEnter Task ID to view details: ")
        )

    except ValueError:
        print("Invalid Task ID.")
        return

    selected_task = None

    for task in subject_tasks:
        if task["id"] == task_id:
            selected_task = task
            break

    if selected_task is None:
        print("Task not found.")
        return

    print("\n========================================")
    print("             TASK DETAILS")
    print("========================================")

    print(f"Task ID: {selected_task['id']}")
    print(f"Title: {selected_task['title']}")
    print(f"Subject: {selected_subject['name']}")
    print(f"Due Date: {selected_task['due_date']}")
    print(f"Due Time: {selected_task['due_time']}")
    print(f"Status: {selected_task['status']}")
    while True:
        choice = input(f"\n[+] Add another task [C] Cancel / Back to Main Menu\n\nSelect: ").strip().lower()
        if choice == "+":
            search_assignment(data)
            return
        elif choice == "c":
            return
        else:
            print(errors)
            print("Invalid option. Enter + or C.")
            print(errors)
# ============================================================
# UPDATE TASK
# ============================================================

def update_task(data):
    # PRINT THE HEADER NG UPDATE TASK FUNCTION
    print(double)
    print(f"{'UPDATE TASK':^40}")
    print(double)

    # CHECK IF MAY TASKS BA SA MAIN DATA
    # KAPAG WALA, WALA DIN TAYONG PWEDE I-UPDATE
    if not data["tasks"]:
        print(sub)
        print("No tasks available to update.")
        print(sub)
        return

    # ----------------------------------------
    # SELECT SUBJECT
    # ----------------------------------------

    print("\nSubjects:")

    # THIS VARIABLE WILL HOLD THE SUBJECT NA PINILI NG USER
    selected_subject = None

    # THIS LIST WILL HOLD THE SUBJECT NAMES
    # GINAGAMIT NATIN ITO PARA MAKUHA YUNG NUMBER OF SUBJECTS
    selected_subj_list = []

    # GET ALL SUBJECTS FROM THE MAIN DATA
    for subject in data["subjects"]:

        # PRINT THE SUBJECT ID AND SUBJECT NAME
        print(f"[{subject['id']}] {subject['name']}")

        # ADD THE SUBJECT NAME TO THE LIST
        selected_subj_list.append(subject["name"])

    # GET THE NUMBER OF SUBJECTS
    # HALIMBAWA MAY 4 SUBJECTS, ANG rangeVal AY 4
    rangeVal = len(selected_subj_list)

    # KEEP ASKING UNTIL THE USER ENTERS A VALID SUBJECT ID
    while True:
        try:
            # ASK THE USER TO ENTER THE SUBJECT ID
            subject_id = int(input("\nEnter Subject ID: "))

            # CHECK IF THE ENTERED ID IS WITHIN THE AVAILABLE SUBJECT ID RANGE
            if subject_id not in range(1, rangeVal + 1):

                # IF INVALID, PRINT THE VALID RANGE
                print(f"Select Option Between (1 - {rangeVal})")

        except ValueError:
            # THIS HANDLES THE ERROR KAPAG HINDI NUMBER ANG ININPUT
            print("Invalid Subject ID.")
            continue

        # CHECK EACH SUBJECT FROM THE MAIN DATA
        for subject in data['subjects']:

            # COMPARE THE ENTERED SUBJECT ID TO THE SUBJECT ID
            if subject_id == subject['id']:

                # IF SAME, STORE THE SUBJECT SA selected_subject
                selected_subject = subject

                # STOP THE FOR LOOP
                break

        # CHECK IF MAY NAPILING SUBJECT
        if selected_subject is not None:

            # IF MERON, STOP THE WHILE LOOP
            break

    # ----------------------------------------
    # SHOW TASKS
    # ----------------------------------------

    # THIS LIST WILL HOLD ALL TASKS
    # NA BELONG SA SELECTED SUBJECT
    subject_tasks = []

    # GET ALL TASKS FROM THE MAIN DATA
    for task in data["tasks"]:

        # CHECK KUNG YUNG TASK AY BELONG SA SELECTED SUBJECT
        if task["subject_id"] == subject_id:

            # IF SAME ANG SUBJECT ID, ADD THE TASK TO subject_tasks
            subject_tasks.append(task)

    # PRINT THE NAME OF THE SELECTED SUBJECT
    print(f"\n--- {selected_subject['name']} ---")

    # CHECK IF WALANG TASKS SA SUBJECT
    if not subject_tasks:
        print(sub)
        print("No tasks for this subject.")
        print(sub)

        # CALL THE FUNCTION AGAIN PARA MAKAPILI NG IBANG SUBJECT
        update_task(data)

    # THIS VARIABLE WILL HOLD THE TASK NA I-E-EDIT NG USER
    selected_task = None

    # SHOW ALL TASKS UNDER THE SELECTED SUBJECT
    for task in subject_tasks:

        # PRINT THE TASK ID AND TITLE
        print(f"[{task['id']}] {task['title']}")

    # KEEP ASKING UNTIL VALID TASK ID ANG ENTERED
    while True:
        try:
            # ASK THE USER FOR THE TASK ID
            task_id = int(input("\nEnter Task ID to edit: "))

        except ValueError:
            # HANDLE THE ERROR KAPAG HINDI NUMBER ANG INPUT
            print("Invalid Task ID.")

        # CHECK EACH TASK SA SELECTED SUBJECT
        for task in subject_tasks:

            # COMPARE THE ENTERED TASK ID
            if task["id"] == task_id:

                # IF SAME, STORE THE TASK SA selected_task
                selected_task = task

                # STOP THE FOR LOOP
                break

        # CHECK IF WALANG NAKITANG TASK
        if selected_task is None:

            # PRINT ERROR MESSAGE
            print("Task not found.")

        else:
            # IF MAY NAKITANG TASK, STOP THE WHILE LOOP
            break

    # ----------------------------------------
    # CATEGORY SELECTION
    # ----------------------------------------

    print("\nCategories you can edit:")

    # KEEP ASKING UNTIL VALID CATEGORY ANG MAPILI
    while True:

        # SHOW ALL AVAILABLE CATEGORIES
        for i, category in enumerate(categories, 1):

            # PRINT THE NUMBER AND CATEGORY NAME
            print(f"[{i}] {category.title()}")

        try:
            # ASK THE USER TO SELECT A CATEGORY
            category_choice = int(input("\nEnter category number: "))

            # CHECK IF VALID ANG CATEGORY NUMBER
            if category_choice not in range(1, len(categories) + 1):

                # GET THE NUMBER OF AVAILABLE CATEGORIES
                length = len(categories)

                # PRINT THE VALID RANGE
                print(f"Select Category between [1 - {length}].")

            # GET THE CATEGORY FROM THE LIST
            # MINUS 1 KASI ANG LIST INDEX STARTS AT 0
            selected_category = categories[category_choice - 1]

            # ----------------------------------------
            # TITLE
            # ----------------------------------------

            # CHECK IF TITLE ANG GUSTONG I-UPDATE
            if selected_category == "title":

                # SHOW THE CURRENT TITLE
                print(f"\nCurrent Title: {selected_task['title']}")

                # ASK THE USER FOR THE NEW TITLE
                new_value = input("Enter new title: ").strip()

                # CHECK IF EMPTY ANG NEW TITLE
                if not new_value:
                    print("Title cannot be empty.")

                # UPDATE THE TITLE OF THE SELECTED TASK
                selected_task["title"] = new_value

            # ----------------------------------------
            # SUBJECT
            # ----------------------------------------

            # CHECK IF SUBJECT ANG GUSTONG I-UPDATE
            elif selected_category == "subject":

                # SHOW THE CURRENT SUBJECT
                print(f"\nCurrent Subject: {selected_subject['name']}")

                print("\nAvailable Subjects:")

                # SHOW ALL AVAILABLE SUBJECTS
                for subject in data["subjects"]:
                    print(f"[{subject['id']}] {subject['name']}")

                try:
                    # ASK THE USER FOR THE NEW SUBJECT ID
                    new_subject_id = int(input("Enter new Subject ID: "))

                except ValueError:
                    # HANDLE THE ERROR KAPAG HINDI NUMBER ANG INPUT
                    print("Invalid Subject ID.")
                    return

                # THIS VARIABLE WILL CHECK IF VALID ANG NEW SUBJECT
                valid_subject = False

                # CHECK ALL SUBJECTS
                for subject in data["subjects"]:

                    # COMPARE THE ENTERED SUBJECT ID
                    if subject["id"] == new_subject_id:

                        # IF FOUND, CHANGE valid_subject TO TRUE
                        valid_subject = True

                        # STOP THE LOOP
                        break

                # CHECK IF INVALID ANG SUBJECT
                if not valid_subject:

                    # PRINT ERROR MESSAGE
                    print("Subject not found.")

                    # RETURN TO MAIN MENU
                    return

                # UPDATE THE SUBJECT ID OF THE TASK
                selected_task["subject_id"] = new_subject_id

            # ----------------------------------------
            # DUE DATE
            # ----------------------------------------

            # CHECK IF DUE DATE ANG GUSTONG I-UPDATE
            elif selected_category == "due date":

                # SHOW THE CURRENT DUE DATE
                print(f"\nCurrent Due Date: {selected_task['due_date']}")

                # KEEP ASKING UNTIL VALID ANG DATE
                while True:

                    # ASK FOR THE NEW DATE
                    new_date = input(
                        "Enter new date (MM/DD/YYYY): "
                    ).strip()

                    try:
                        # CHECK IF VALID ANG DATE FORMAT
                        datetime.strptime(new_date, "%m/%d/%Y")

                        # IF VALID, STOP THE LOOP
                        break

                    except ValueError:
                        # IF INVALID, PRINT ERROR MESSAGE
                        print("Invalid date. Example: 09/30/2026")

                # SHOW THE CURRENT DUE TIME
                print(f"Current Due Time: {selected_task['due_time']}")

                # KEEP ASKING UNTIL VALID ANG TIME
                while True:

                    # ASK FOR THE NEW TIME
                    new_time = input(
                        "Enter new time (HH:MM AM/PM): "
                    ).strip()

                    try:
                        # CHECK IF VALID ANG TIME FORMAT
                        datetime.strptime(new_time, "%I:%M %p")

                        # IF VALID, STOP THE LOOP
                        break

                    except ValueError:
                        # IF INVALID, PRINT ERROR MESSAGE
                        print("Invalid time. Example: 10:30 PM")

                # UPDATE THE DUE DATE
                selected_task["due_date"] = new_date

                # UPDATE THE DUE TIME
                selected_task["due_time"] = new_time

            # ----------------------------------------
            # STATUS
            # ----------------------------------------

            # CHECK IF STATUS ANG GUSTONG I-UPDATE
            elif selected_category == "status":

                # SHOW THE CURRENT STATUS
                print(f"\nCurrent Status: {selected_task['status']}")

                print("\nAvailable Status:")

                # SHOW ALL AVAILABLE STATUS
                for index, status in enumerate(STATUS_OPTIONS, 1):
                    print(f"[{index}] {status}")

                # KEEP ASKING UNTIL VALID STATUS ANG INPUT
                while True:
                    try:
                        # ASK THE USER FOR THE NEW STATUS NUMBER
                        new_status_choice = int(
                            input("Enter new status: ")
                        )

                        # CHECK IF THE INPUT IS WITHIN 1 TO 3
                        if new_status_choice not in range(
                            1, len(STATUS_OPTIONS) + 1
                        ):
                            print("Invalid status.")

                        # IF VALID, STOP THE LOOP
                        break

                    except ValueError:
                        # HANDLE THE ERROR KAPAG HINDI NUMBER
                        print("Invalid status.")

                # GET THE STATUS FROM STATUS_OPTIONS
                # MINUS 1 KASI INDEXING STARTS AT 0
                print(
                    f"Your New Status is :"
                    f"{STATUS_OPTIONS[new_status_choice - 1]}"
                )

                # UPDATE THE STATUS OF THE SELECTED TASK
                selected_task["status"] = STATUS_OPTIONS[
                    new_status_choice - 1
                ]

        except ValueError:
            # HANDLE THE ERROR KAPAG INVALID ANG CATEGORY INPUT
            print("\nInvalid category.")

        # ----------------------------------------
        # AFTER UPDATE
        # ----------------------------------------

        # ASK THE USER IF THEY WANT TO UPDATE ANOTHER TASK
        while True:

            # SHOW THE AVAILABLE OPTIONS
            print(f"\n{'[+] Update Other task'} {'[C] Cancel'}")

            # ASK THE USER TO SELECT AN OPTION
            option = input("\nSELECT : ").strip().lower()

            # MATCH THE INPUT TO THE AVAILABLE OPTIONS
            match option:

                # IF "+" ANG INPUT, UPDATE ANOTHER TASK
                case "+":
                    update_task(data)

                # IF "c", SAVE THE DATA AND RETURN TO MAIN MENU
                case "c":
                    save_data(data)

                    print("\nTask edited successfully!")

                    return

                # IF INVALID ANG INPUT
                case _:
                    print("Invalid option. Enter + or C.")


# ============================================================
# DELETE TASK
# ============================================================

def delete_task(data):

    # PRINT THE DELETE TASK HEADER
    print("\n========================================")
    print(f"{'DELETE TASK':<40}")
    print("========================================")

    # CHECK IF MAY TASKS BA SA MAIN DATA
    if not data["tasks"]:

        # IF WALANG TASK, PRINT MESSAGE
        print("No tasks available.")

        # RETURN TO MAIN MENU
        return

    # ----------------------------------------
    # SELECT SUBJECT
    # ----------------------------------------

    print("\nSubjects:")

    # SHOW ALL SUBJECTS
    for subject in data["subjects"]:

        # PRINT SUBJECT ID AND SUBJECT NAME
        print(f"[{subject['id']}] {subject['name']}")

    try:
        # ASK THE USER FOR SUBJECT ID
        subject_id = int(
            input("\nEnter Subject ID: ")
        )

    except ValueError:
        # HANDLE THE ERROR KAPAG HINDI NUMBER ANG INPUT
        print("Invalid Subject ID.")
        return

    # THIS LIST WILL HOLD TASKS UNDER THE SELECTED SUBJECT
    subject_tasks = []

    # CHECK ALL TASKS FROM THE MAIN DATA
    for task in data["tasks"]:

        # CHECK IF THE TASK BELONGS TO THE SELECTED SUBJECT
        if task["subject_id"] == subject_id:

            # ADD THE TASK TO subject_tasks
            subject_tasks.append(task)

    # CHECK IF WALANG TASK SA SUBJECT
    if not subject_tasks:

        # PRINT MESSAGE
        print("No tasks found for this subject.")

        # RETURN TO MAIN MENU
        return

    # ----------------------------------------
    # SHOW TASKS
    # ----------------------------------------

    print("\nTasks:")

    # SHOW ALL TASKS UNDER THE SELECTED SUBJECT
    for task in subject_tasks:

        # PRINT TASK ID AND TITLE
        print(
            f"[{task['id']}] "
            f"{task['title']}"
        )

    try:
        # ASK THE USER FOR THE TASK ID TO DELETE
        task_id = int(
            input("\nEnter Task ID to delete: ")
        )

    except ValueError:
        # HANDLE THE ERROR KAPAG HINDI NUMBER
        print("Invalid Task ID.")
        return

    # THIS VARIABLE WILL HOLD THE TASK NA I-DE-DELETE
    selected_task = None

    # CHECK ALL TASKS FROM THE MAIN DATA
    for task in data["tasks"]:

        # CHECK BOTH TASK ID AND SUBJECT ID
        # PARA SIGURADO NA TAMANG TASK ANG MA-DELETE
        if (
            task["id"] == task_id
            and task["subject_id"] == subject_id
        ):

            # STORE THE MATCHING TASK
            selected_task = task

            # STOP THE LOOP
            break

    # CHECK IF WALANG NAKITANG TASK
    if selected_task is None:

        # PRINT ERROR MESSAGE
        print("Task not found.")

        # RETURN TO MAIN MENU
        return

    # ----------------------------------------
    # DELETE CONFIRMATION
    # ----------------------------------------

    # ASK THE USER TO CONFIRM BEFORE DELETING
    confirm = input(
        f"\nDelete '{selected_task['title']}'? "
        "[Y/N]: "
    ).strip().lower()

    # CHECK IF USER CONFIRMED WITH "Y"
    if confirm == "y":

        # REMOVE THE SELECTED TASK FROM THE TASKS LIST
        data["tasks"].remove(selected_task)

        # SAVE THE UPDATED DATA TO JSON FILE
        save_data(data)

        # SHOW SUCCESS MESSAGE
        print("\nTask deleted successfully!")

    else:
        # IF USER DID NOT ENTER "Y", CANCEL THE DELETE
        print("\nDelete cancelled.")

    # ----------------------------------------
    # DELETE ANOTHER TASK
    # ----------------------------------------

    # ASK THE USER IF THEY WANT TO DELETE ANOTHER TASK
    while True:

        # SHOW AVAILABLE OPTIONS
        print(f"{'[+] Update Other task'} {'[C] Cancel'}")

        # ASK THE USER FOR THEIR CHOICE
        choice = input("Select: ")

        # IF "+" ANG INPUT
        if choice == "+":

            # CALL THE DELETE FUNCTION AGAIN
            delete_task(data)

            # RETURN AFTER THE FUNCTION FINISHES
            return

        # IF "C" ANG INPUT
        elif choice == "c":

            # RETURN TO MAIN MENU
            return

        else:
            # IF INVALID ANG INPUT, PRINT ERROR MESSAGE
            print(errors)
            print("Invalid option. Enter + or C.")
            print(errors)


# ============================================================
# PROGRAM START
# ============================================================

def main():

    # LOAD THE EXISTING DATA FROM THE JSON FILE
    # KUNG WALA PA, GAGAWA ITO NG DEFAULT DATA
    data = load_data()

    # SET UP THE STUDENT INFORMATION
    # DITO KINUKUHA ANG NAME, COURSE, AT SUBJECTS
    setup_student(data)

    # AFTER SETUP, RUN THE MAIN MENU
    # DITO NA MAKIKITA ANG MAIN FUNCTIONS NG SYSTEM
    main_menu(data)


# THIS CHECKS IF THIS FILE IS BEING RUN DIRECTLY
if __name__ == "__main__":

    # IF TRUE, CALL THE main() FUNCTION
    main()
