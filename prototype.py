import json


assignments = []
status = ["Pending", "Processing", "Complete"]
file = "tasks.json"

def main():
    load_assignments()
    main_Menu()

def load_assignments():
    global assignments

    try:
        with open("tasks.json", "r") as file:
            assignments = json.load(file)

            if not isinstance(assignments, list):
                assignments = []

    except FileNotFoundError:
        assignments = []
        save_assignments()

    except json.JSONDecodeError:
        print("Warning: tasks.json contains invalid data.")
        assignments = []


def save_assignments():
    try:
        with open("tasks.json", "w") as file:
            json.dump(assignments, file, indent=4)

    except OSError as error:
        print(f"Error saving assignments: {error}")



def main_Menu():
    main_menu = [
                "Add New Task",
                "View All Task",
                "Search Assignment",
                "Update Task Status",
                "Delete Task",
                "Exit"
            ]

    

            
    while True:
        print("\n======================")
        print("SMART TASK ALERT")
        print("Digital Assignment Monitoring")
        print("and Reminder System")
        print("\n======================")
        for i,category in enumerate(main_menu):
            print(f"{[i + 1]}. {category}")
        
        try:
            choice = int(input("\nSelect Option: "))
            if choice == 1:
                add_assignment()
            elif choice == 2:
                view_assignments()
            elif choice == 3:
                search_assignment()
            elif choice == 4:
                update_task()
                print("Update Assignment")
            elif choice == 5:
                delete_task()
                print ("Delete Assignment")
            elif choice == 6:
                print("Thank you for using SmartTask Alert!")
                break
            else:
                print("Invalid Input!")
                print("Please choose a number from 1 to 6.")
        except ValueError:
            print("Invalid Input!")
            print("Please enter a valid number.")

def add_assignment():
    title = input("Enter assignment title: ")
    subject = input("Enter subject: ")
    due_date = input("Enter Deadline: ")
    print(f"\nPlease select an option for status of your Task:")
    try:
        for index,stat in enumerate(status):
            print(f"Enter [{index +1}] for {stat}")
            
        stats = int(input("Enter Status for this Task: ")) - 1
        
        stat_index = len(status)
        if stats in range(stat_index):
            task_status = status[stats]
            assignment = {"title": title,
                  "subject": subject,
                  "deadline": due_date,
                  "Status": task_status
                }
            assignments.append(assignment)
            save_assignments()
            print("Assignment added successfully!")
        return assignments
    except ValueError:
        print("enter a valid number for Status!")

def view_assignments():
    print("\n--- Assignment List ---*")

    if assignments is None or not assignments:
        print("No assignments found.")
        return
    
    header = list(assignments[0].keys())
    header_formatted_text = " | ".join(f"{item:<10}" for item in header)
    print(f"{'ID No.':<10}| {header_formatted_text}")
    print("-" * 50)

    for i, tasks in enumerate(assignments):
        print(f"ID {i + 1:<6} | {tasks['title']:<10} | {tasks['subject']:<10} | {tasks['deadline']:<10} | {tasks['Status']:<1}")




    """ # print(f"{i}. {assignment['title']}")
        # print(f"Subject: {assignment ['subject' ]}")
        # print(f"deadline: {assignment ['deadline' ]}")"""

def search_assignment():
    keyword = input("Enter assignment title to search: ")
    found = False
    for assignment in assignments:
        if keyword. lower() in assignment["title"]. lower():
            print("\nAssignment Found!")
            print("Title:"
            , assignment ["title"])
            print("Subject:"
            , assignment ["subject" ])
            print ("deadline:", assignment ["deadline"])
            found = True
            
    if not found:
        print( "Assignment not found.")

def update_task():
    view_assignments()
    select_task_id = int(input("please enter task ID here: ")) - 1
    task_id_index = len(assignments)
    if select_task_id in range(task_id_index):
        tasks = list(assignments[select_task_id].keys())
        print("choose a category to edit")
        for no,task in enumerate(tasks, 1):
            print(f"Id [{no}] {task}")

        try:
            id_input = int(input("Please enter the ID no. here: ")) - 1
            id_value = tasks[id_input]
            
            current_val = assignments[select_task_id][id_value]
            print(f"\nCurrent {current_val}")

            if id_input in range(len(tasks)):
                edit_text = input(f"please enter a new {id_value} here: ")
                assignments[select_task_id][id_value] = edit_text
                save_assignments()

        except ValueError:
            print("please enter a valid option")

def delete_task():
    if not assignments:
        print("No assignments found.")
        return

    view_assignments()

    try:
        idTask_to_remove = int(input("Enter an ID you want to remove: ")) - 1

        if idTask_to_remove in range(len(assignments)):
            removed_task = assignments.pop(idTask_to_remove)
            save_assignments()

            print(f"Deleted assignment: {removed_task['title']}")
        else:
            print("Invalid task ID.")

    except ValueError:
        print("Please enter a valid number.")

"""def delete_task():
    view_assignments()
    idTask_to_remove = int(input("enter an ID you wanted to remove: ")) - 1
    id_range = len(assignments)
    id_index = assignments[idTask_to_remove]
    if idTask_to_remove in range(id_range):
        assignments.remove(id_index)"""

if __name__ == "__main__":
    main()

