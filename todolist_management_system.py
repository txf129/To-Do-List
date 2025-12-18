# I make this to do list for learning python

import os
import emoji
import json
import datetime

class ToDoList():
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Warning: Could not load {self.data_file}. Starting with empty library.")
        return {}
    
    def save_tasks(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                      json.dump(self.tasks, file, indent=2, ensure_ascii=False)
            print(f"Data saved successfully to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_task(self):
        print(emoji.emojize("\n :balloon: Add New Task"))

        print(emoji.emojize(":cyclone: Task's title:"))
        title = input("> ").strip()

        if not title:
            print("Title cannot be empty.")
            return
        
        if title in self.tasks:
            print(f"Task '{title}' already exists. Use 'edit' to modify it...")
            return
        
        print("Details: ")
        details = input("> ").strip()

        print(emoji.emojize(""":round_pushpin: Priority:
        "1. High
         2. Medium 
         3.Low
         Choose a number."""))
        priority_input = input("> ").strip()
        priority = None
        if priority_input == "1":
            try:
                priority = "High"
            except ValueError:
                print("Skipped priority.")
        if priority_input == "2":
            try: 
                priority = "Medium"
            except ValueError:
                print("Skipped priority.")
        if priority_input == "3":
            try:
                priority = "Low"
            except ValueError:
                print("Skipped priority.")

        task = {"title": title, "details": details, "priority": priority}

        self.tasks[title] = task
        self.save_tasks()
        print(emoji.emojize(f"Task '{title}' added successfully. :check_mark_button:"))


    def edit_task(self):
        if not self.tasks:
            print("No tasks in your library yet.")
            return
        
        print(emoji.emojize("\n :pencil: Edit Task"))
        print("All your tasks until here:")
        only_tasks = list(map(str, self.tasks))
        for index, task in enumerate(only_tasks, start=1):
            print(f"{index}: {task}")
            
        print("\nEnter the task's number you wanna edit:")
        choice = input("> ").strip()
        
        if choice.isdigit():
            task_number = int(choice)
            if 1 <= task_number <= len(only_tasks):
                title = only_tasks[task_number - 1]
                print(f"Selected task: {title}")
            else:
                print("Number is out of range.")
        else:
            print("Please enter a number.")

        if title not in self.tasks:
            print(f"Task '{title}' not found.")
            return
        
        task = self.tasks[title]
        print(f"\nEditing: {title}")
        print(f"""      Task's information: 
              Details: {task["details"]}
              Priority: {task["priority"]}
              """)
        print("(While editing you can press Enter to keep the current value.)")

        new_title = input(f"New Title: ").strip()
        if new_title:
            if new_title != title:
                if new_title in self.tasks:
                    print(f"Task '{new_title}' already exists.")
                else:
                    # Updating the key inner dict
                    task["title"] = new_title
                    # Now changing the main key of the dict
                    # Starting with deleting the old key
                    self.tasks.pop(title)
                    # Now adding the new one
                    self.tasks[new_title] = task

                    # Chaning the 'new_title' to 'title' for the rest of the code
                    title = new_title

        new_details = input(f"New Details: ").strip()
        if new_details:
            task["details"] = new_details

        print(f"New priority: ")
        print(emoji.emojize(""":round_pushpin: Priority:
        "1. High
         2. Medium 
         3. Low
         Choose a number."""))
        new_priority_input = input("> ").strip()
        new_priority = None
        if new_priority_input == "1":
            try:
                new_priority = "High"
            except ValueError:
                print("Skipped priority.")
        if new_priority_input == "2":
            try: 
                new_priority = "Medium"
            except ValueError:
                print("Skipped priority.")
        if new_priority_input == "3":
            try:
                new_priority = "Low"
            except ValueError:
                print("Skipped priority.")
        if new_priority:
            task["priority"] = new_priority

        self.save_tasks()
        print(emoji.emojize(f"Task '{title}' updated successfuly. :check_mark_button:"))

    def delete(self):
        if not self.tasks:
            print("No tasks in your library yet.")
            return
        
        print(emoji.emojize("\n :cross_mark_button: Delete Task"))
        print("All your tasks until here:")
        tasks_to_show = self.tasks
        only_tasks = list(map(str, tasks_to_show))
        print(only_tasks)
        print("Enter the task's title you wanna delete:")
        title = input("> ").strip()


        if title not in self.tasks:
            print(f"Task '{title}' not found.")
            return
        
        self.tasks.pop(title)
        print(emoji.emojize(f"Task '{title}' deleted successfully. :check_mark_button:"))
        self.save_tasks()
               
    def show_all_tasks(self, filter_status: str = None):
        if not self.tasks:
            print("No tasks in your todolist yet.")
            return
        
        tasks_to_show = self.tasks

        for i, (task_name, task_data) in enumerate(tasks_to_show.items(), start=1):
            print(f"""  Task no.{i}: {task_name} 
              Details: "{task_data["details"]}"
              Priority: "{task_data["priority"]}"
              """)
    
    def main(self):
        """main loop"""
        print(emoji.emojize(":diamond_with_a_dot: Task Management System"))

        while True:
            print(emoji.emojize("""\n               :large_blue_diamond: Options:
                  1. Add a task
                  2. Edit a task
                  3. Delete a task
                  4. View all tasks (To Do List)
                  5. Quit"""))
            choice = input("\nEnter your choice (1-5) ").strip()

            if choice ==  "1":
                self.add_task()
            elif choice == "2":
                self.edit_task()
            elif choice == "3":
                self.delete()
            elif choice == "4":
                self.show_all_tasks()
            elif choice == "5":
                print(emoji.emojize("Fighting! :fire:"))
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    todolist = ToDoList()
    todolist.main()

