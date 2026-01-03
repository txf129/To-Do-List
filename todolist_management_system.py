import os
import json
import datetime

class Data_Context:
    def __init__(self):
        self.data_file = "tasks.json"
        self.data_file_2 = "rewards.json"
        self.tasks = {}
        self.rewards = {}

class Save_and_load:
    def load_tasks(self, context):
            if os.path.exists(context.data_file):
                try:
                    with open(context.data_file, "r", encoding="utf-8") as file:
                        context.tasks = json.load(file)
                except (json.JSONDecodeError, FileNotFoundError):
                    print(f"Warning: Could not load {context.data_file}. Starting with empty library.")
                    context.tasks = {}
            else:
                context.tasks = {}

    def load_rewards(self, context):
        if os.path.exists(context.data_file_2):
            try:
                with open(context.data_file_2, "r", encoding="utf-8") as file:
                    context.rewards = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Warning: Could not load {context.data_file_2}. Starting with empty library.")
                context.rewards = {}
        else:
            context.rewards = {}

    def save_tasks(self, context):
        try:
            with open(context.data_file, "w", encoding="utf-8") as file:
                json.dump(context.tasks, file, indent=2, ensure_ascii=False)
            print(f"Data saved successfully to {context.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def save_rewards(self, context):
        try:
            with open(context.data_file_2, "w", encoding="utf-8") as file:
                json.dump(context.rewards, file, indent=2, ensure_ascii=False)
            print(f"Data saved successfully to {context.data_file_2}")
        except Exception as e:
            print(f"Error saving data: {e}")

class Actions_Task:
    def __init__(self, save_and_load):
        self.save_and_load = save_and_load

    def add_task(self, context):
        print(("\n📍 Add New Task"))

        print(("🧃 Task's title:"))
        title = input("> ").strip()

        if not title:
            print("Title cannot be empty.")
            return

        if title in context.tasks:
            print(f"Task '{title}' already exists. Use 'edit' to modify it...")
            return

        print("📂 Details: ")
        details = input("> ").strip()

        print(("""🎯 Priority:
            1. High
            2. Medium 
            3. Low"""))
        print("Choose a number.")
        priority_input = input("> ").strip()
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

        print("💥 How demanding does this task feel?")
        print(("""         1. 🔵 Light Effort
                            (Quick wins & low mental drag)
                            - Takes minimal focus
                            - Can be done even tired or between sessions
                            - Examples: Tidy your desk, skim an article, reply to an email, order Xs online."""))
        print(("""         2. 🟢 Medium Effort
                            (Focused work that needs engagement)
                            - Requires dedicated attention
                            - Likely 30 minutes to 2 hours
                            - You'll need to "get in the zone" """))
        print(("""         3. 🟣 Heavy Effort
                            - Deep, immersive, and fragile
                            - Best scheduled for your personal peak focus times
                            - Requires shielding from interruptions."""))

        print("Choose a number.")
        effort_input = input("> ")

        if effort_input == "1":
            try:
                effort = "Light"
            except ValueError:
                print("Skipped Effort.")
        if effort_input == "2":
            try: 
                effort = "Medium"
            except ValueError:
                print("Skipped Effort.")
        if effort_input == "3":
            try:
                effort = "Heavy"
            except ValueError:
                print("Skipped Effort.")

        print(("🗃️  Now determine your task's status."))
        print("Choose from the menu:")
        print("""
                1. Just added
                2. On Progress
                3. Completed
                4. Cancelled""")

        status_input = input("> ").strip()

        if status_input == "1":
            try:
                status = "Just added"
            except ValueError:
                print("Skipped status.")
        if status_input == "2":
            try:
                status = "On Progress"
            except ValueError:
                print("Skipped status.")
        if status_input == "3":
            try:
                status = "Completed"
            except ValueError:
                print("Skipped status.")
        if status_input == "4":
            try:
                status = "Cancelled"
            except ValueError:
                print("Skipped status.")

        task_start_date = str(datetime.date.today())

        print("🗓️  And finally, what about the Due Date for your task?")
        print("Use this format please to write the date. (29 Apr, 2075)")
        while True: 
            task_due_date_string = input("> ")
            checking_format = "%d %b, %Y"
            try: 
                parsed_date = datetime.datetime.strptime(task_due_date_string, checking_format)
                task_due_date = str(parsed_date.date())
                break
            except ValueError:
                print("Please enter a valid date in the format: 29 Apr, 2075")

        task = {"title": title, "details": details, "priority": priority, "effort": effort, "status": status, "start_date": task_start_date, "due_date": task_due_date}

        context.tasks[title] = task
        self.save_and_load.save_tasks(context)
        sync_rewards_with_tasks(context, self.save_and_load)
        print((f"Task '{title}' added successfully. ✔️"))

    def update_task_status(self, context):
        if not context.tasks:
            print("No tasks in your library yet.")
            return
        
        print("Update Task Status:")
        print("All your tasks until here:")
        only_tasks = list(context.tasks.keys())
        for index, task in enumerate(only_tasks, start=1):
            print(f"{index}: {task}")
            
        print("\nEnter the task's number you wanna update:")
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
        
        if title not in context.tasks:
            print(f"Task '{title}' not found.")
            return
        
        task = context.tasks[title]
        print(f"\n🔷 Updating Status: {title}")
        print(f"""      \nTask's Status information: 
               "{task["status"]}" """)
        print("(While editing you can press Enter to keep the current value.)")
        print(f"Please choose from the menu: ")
        print(("""Status:
              1. Just added
              2. On Progress
              3. Completed
              4. Cancelled"""))
        
        new_status_input = (input("> ").strip())

        if new_status_input == "1":
            try:
                new_status = "Just added"
            except ValueError:
                print("Skipped status.")
        if new_status_input == "2":
            try:
                new_status = "On Progress"
            except ValueError:
                print("Skipped status.")
        if new_status_input == "3":
            try:
                new_status = "Completed"
            except ValueError:
                print("Skipped status.")
        if new_status_input == "4":
            try:
                new_status = "Cancelled"
            except ValueError:
                print("Skipped status.")
        if new_status:
            task["status"] = new_status

        self.save_and_load.save_tasks(context)
        sync_rewards_with_tasks(context, self.save_and_load)
        print((f"Task '{title}' updated successfuly. ✔️"))

    def edit_task(self, context):
        if not context.tasks:
            print("No tasks in your library yet.")
            return
        
        print(("\n ✏️ Edit Task"))
        print("🔶 All your tasks until here:")
        only_tasks = list(context.tasks.keys())
        for index, task in enumerate(only_tasks, start=1):
            print(f"{index}: {task}")
            
        print("\n🔷 Enter the task's number you wanna edit:")
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

        if title not in context.tasks:
            print(f"Task '{title}' not found.")
            return
        
        task = context.tasks[title]
        print(f"\n🔷 Editing: {title}")
        print(f"""      Task's information: 
              Details: {task["details"]}
              Priority: {task["priority"]}
              Effort: "{task["effort"]}"
              Status: "{task["status"]}"
              Start date: "{task["start_date"]}"
              Due date: "{task["due_date"]}"
              """)
        print("(While editing you can press Enter to keep the current value.)")

        new_title = input(f"New Title: ").strip()
        if new_title:
            if new_title != title:
                if new_title in context.tasks:
                    print(f"Task '{new_title}' already exists.")
                else:
                    # Updating the key inner dict
                    task["title"] = new_title
                    # Now changing the main key of the dict
                    # Starting with deleting the old key
                    context.tasks.pop(title)
                    # Now adding the new one
                    context.tasks[new_title] = task

                    # Chaning the 'new_title' to 'title' for the rest of the code
                    title = new_title

        new_details = input(f"New Details: ").strip()
        if new_details:
            task["details"] = new_details

        print(f"🔷 New priority: ")
        print(("""1. High
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
            if new_priority:
                task["priority"] = new_priority
        if new_priority_input == "2":
            try: 
                new_priority = "Medium"
            except ValueError:
                print("Skipped priority.")
            if new_priority:
                task["priority"] = new_priority
        if new_priority_input == "3":
            try:
                new_priority = "Low"
            except ValueError:
                print("Skipped priority.")
            if new_priority:
                task["priority"] = new_priority

        print("🔷 New Effort Level: ")
        print(("""1. 🔵 Light Effort
                            (Quick wins & low mental drag)
                            - Takes minimal focus
                            - Can be done even tired or between sessions
                            - Examples: Tidy your desk, skim an article, reply to an email, etc."""))
        print(("""2. 🟢 Medium Effort
                            (Focused work that needs engagement)
                            - Requires dedicated attention
                            - You'll need to "get in the zone" 
                            - Examples: Write a blog post section, Studying X, Outline a project's next phase"""))
        print(("""3. 🟣 Heavy Effort
                            (Deep work that demands planning & peak energy)
                            - Deep, immersive, and fragile
                            - Best scheduled for your personal peak focus times
                            - Requires shielding from interruptions."""))

        print("Choose a number.")
        new_effort_input = input("> ")

        if new_effort_input == "1":
            try:
                new_effort = "Light"
            except ValueError:
                print("Skipped priority.")
            if new_effort:
                task["effort"] = new_effort
        if new_effort_input == "2":
            try: 
                new_effort = "Medium"
            except ValueError:
                print("Skipped priority.")
            if new_effort:
                task["effort"] = new_effort
        if new_effort_input == "3":
            try:
                new_effort = "Heavy"
            except ValueError:
                print("Skipped priority.")
            if new_effort:
                task["effort"] = new_effort

        print(f"🔷 New status: ")
        print(("""1. Just added
              2. On Progress
              3. Completed
              4. Cancelled"""))
        
        new_status_input = (input("> ").strip())

        if new_status_input == "1":
            try:
                new_status = "Just added"
            except ValueError:
                print("Skipped status.")
            if new_status:
                task["status"] = new_status
        if new_status_input == "2":
            try:
                new_status = "On Progress"
            except ValueError:
                print("Skipped status.")
            if new_status:
                task["status"] = new_status
        if new_status_input == "3":
            try:
                new_status = "Completed"
            except ValueError:
                print("Skipped status.")
            if new_status:
                task["status"] = new_status
        if new_status_input == "4":
            try:
                new_status = "Cancelled"
            except ValueError:
                print("Skipped status.")
            if new_status:
                task["status"] = new_status

        print("🔷 Setting a new 'Start Date': ")
        print("Please keep in mind to use this format to write the date. (11 Aug, 1950)")
        new_task_start_date_string = ""
        if new_task_start_date_string:
            new_task_start_date_string = input("> ")
            checking_format = "%d %b, %Y"
            try:
                parsed_date = datetime.datetime.strptime(new_task_start_date_string, checking_format)
                new_task_start_date = str(parsed_date.date())
            except ValueError:
                print("Skipped Start Date")
                new_task_start_date_string = ""
            if new_task_start_date:
                task["start_date"] = new_task_start_date
        
        print("🔷 Setting a new 'Due Date': ")
        print("Please keep in mind to use this format to write the date. (23 Jul, 2001)")
        new_task_due_date_string = ""
        if new_task_due_date_string:
            new_task_due_date_string = input("> ")
            checking_format = "%d %b, %Y"
            try:
                parsed_date = datetime.datetime.strptime(new_task_due_date_string, checking_format)
                new_task_due_date = str(parsed_date.date())
            except ValueError:
                print("Skipped Due Date")
                new_task_due_date_string = ""
            if new_task_due_date:
                task["due_date"] = new_task_due_date

        context.save_tasks()
        sync_rewards_with_tasks(context, self.save_and_load)
        print((f"Task '{title}' updated successfuly. ✔️"))

    def delete(self, context):
        if not context.tasks:
            print("No tasks in your library yet.")
            return
        
        print("🔶 All your tasks until here:")
        only_tasks = list(context.tasks.keys())
        for index, task in enumerate(only_tasks, start=1):
            print(f"{index}: {task}")
            
        print("\n🔷 Enter the task's number you wanna edit:")
        choice = input("> ").strip()
        
        if choice.isdigit():
            task_number = int(choice)
            if 1 <= task_number <= len(only_tasks):
                title = only_tasks[task_number - 1]
                print(f"Selected task: {title}")
            else:
                print("Number is not in the range.")
        else:
            print("Please enter a number.")

        if title not in context.tasks:
            print(f"Task '{title}' not found.")
            return
        
        confirm = input("Are you sure you want to delete this task? (yes/no)").strip().lower()
        if confirm == "yes":
            context.tasks.pop(title)
            self.save_and_load.save_tasks(context)
            sync_rewards_with_tasks(context, self.save_and_load)
            print((f"Task '{title}' deleted successfully. ✔️"))
        else: 
            print("Deletion cancelled.")
               
    def show_all_tasks(self, context, filter_status: str = None):
        if not context.tasks:
            print("No tasks in your todolist yet.")
            return
        
        tasks_to_show = context.tasks.items()

        for i, (task_name, task_data) in enumerate(tasks_to_show, start=1):
            print(f"""  Task no.{i}: {task_name} 
              Details: "{task_data["details"]}"
              Priority: "{task_data["priority"]}"
              Effort: "{task_data["effort"]}"
              Status: "{task_data["status"]}"
              Start date: "{task_data["start_date"]}"
              Due date: "{task_data["due_date"]}"
              """)

class Reward:
    def __init__(self, save_and_load):
        self.save_and_load = save_and_load

    def reward(self, context):
        while True:
            print("""Options: 
            1. Add Reward
            2. Show all Rewards
            3. Delete Reward
            4. Claim Reward
            5. Exit""")

            choice = input("\nEnter your choice (1-5) ").strip()

            if choice ==  "1":
                self.add_reward(context)
            elif choice == "2":
                self.reward_show(context)
            elif choice == "3":
                self.reward_delete(context)
            elif choice == "4":
                self.claim_reward(context)
            elif choice == "5":
                print("Exiting Reward Section.")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_reward(self, context):
        print("Reward:")
        print("""In this section, you can add some rewards for smashing your tasks.""")

        print("Select how do you want to see your tasks:")
        print("1. Just titles")
        print("2. Full information")

        try:
            user_input = input("> ").strip()

            if not context.tasks:
                print("No tasks in your todolist yet.")
                return

            if user_input == "1":
                tasks_list = list(context.tasks.keys())
                for index, task_name in enumerate(tasks_list, start=1):
                    task_status = context.tasks[task_name]["status"]
                    status_symbol = "✓" if task_status == "Completed" else "✗"
                    print(f"{index}: {task_name} [{status_symbol}]")
               
            elif user_input == "2":
                for i, (task_name, task_data) in enumerate(context.tasks.items(), start=1):
                    status_symbol = "✓" if task_data["status"] == "Completed" else "✗"
                    print(f"""Task no.{i}: {task_name} [{status_symbol}]
                    Details: "{task_data["details"]}"
                    Priority: "{task_data["priority"]}"
                    Effort: "{task_data["effort"]}"
                    Status: "{task_data["status"]}"
                    Start date: "{task_data["start_date"]}"
                    Due date: "{task_data["due_date"]}" """)
            
            else:
                print("Invalid option.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

        print("""Treat yourself! \nSet a personal reward, then add the tasks you need to finish to earn it.""")
        reward_name = input("Enter reward name: ").strip()
        if reward_name in context.rewards:
            print(f"Reward '{reward_name}' already exists. You can use 'edit' to modify it...")
            return

        print("\nYour available tasks:")
        tasks_list = list(context.tasks.keys())
        for index, task_name in enumerate(tasks_list, start=1):
            task_status = context.tasks[task_name]["status"]
            is_completed = task_status == "Completed"
            status_symbol = "✓" if is_completed else "✗"
            print(f"{index}: {task_name} [{status_symbol}]")
        
        print("\nEnter the numbers of tasks to associate with this reward (comma-separated, e.g., 1,3,5):")

        try: 
            task_numbers_input = input("> ").strip()

            if not task_numbers_input:
                print("No tasks selected.")
                return
            
            task_numbers = [int(num.strip()) for num in task_numbers_input.split(",")]

            related_tasks = {}
            for num in task_numbers:
                if 1 <= num <= len(tasks_list):
                    task_name = tasks_list[num - 1]
                    task_status = context.tasks[task_name]["status"]
                    is_completed = task_status == "Completed"
                    related_tasks[task_name] = is_completed
                else:
                    print(f"Task number {num} is invalid. Skipping...")
            if not related_tasks:
                print("No valid tasks selected.")
                return

            context.rewards[reward_name] = related_tasks

            reward_status = self.calculate_reward_status(context, reward_name)

            self.save_and_load.save_rewards(context)
            print(f"\nReward '{reward_name}' added successfully!")
            print(f"Associated tasks: {",".join(related_tasks.keys())}")
            print(f"Current completion: {sum(related_tasks.values())}/{len(related_tasks)} tasks")

            if reward_status:
                print("This reward is now available!")
        except ValueError:
            print("Please enter valid numbers separated by commas.")

    def calculate_reward_status(self, context, reward_name):
        if reward_name not in context.rewards:
            return False
        related_tasks = context.rewards[reward_name]
        return all(related_tasks.values())

    def reward_show(self, context):
        if not context.rewards:
            print("No rewards have been created yet.")
            return
        
        print("Your Rewards:\n")

        for i, (reward_name, tasks_dict) in enumerate(context.rewards.items(), start=1):
            completed_count = sum(tasks_dict.values())
            total_tasks = len(tasks_dict)
            reward_available = self.calculate_reward_status(context, reward_name)

            status_symbol = "🎁 AVAILABLE" if reward_available else "🔒 LOCKED"
            print(f"{i}. {reward_name} - {status_symbol}")
            print(f"   Progress: {completed_count}/{total_tasks} tasks completed")
            
            for task_name, is_completed in tasks_dict.items():
                status_symbol = "✅" if is_completed else "❌"
                task_info = f"      {status_symbol} {task_name}"

                if task_name in context.tasks:
                    task_details = context.tasks[task_name]
                    task_info += f" (Priority: {task_details["priority"]}, Due: {task_details["due_date"]})"
                    print(task_info)
            
            if reward_available:
                print(f"\n Congratulations!🎉 You can now claim '{reward_name}'!")
            elif completed_count > 0:
                remaining = total_tasks - completed_count
                print(f"\n Keep going! 🦾 Only {remaining} task(s) left to earn. '{reward_name}'")
            print()
    
    def claim_reward(self, context):
        if not context.rewards:
            print("No rewards have been created yet.")
            return

        available_rewards = []
        for reward_name, tasks_dict in context.rewards.items():
            if self.calculate_reward_status(context, reward_name):
                available_rewards.append(reward_name)
        
        if not available_rewards:
            print("No rewards are available to claim yet.")
            print("Complete more tasks to earn rewards!")
            return
        
        print("Available rewards to claim:")
        for i, reward_name in enumerate(available_rewards, start=1):
            print(f"{i}. {reward_name}")
        
        try:
            choice = input("\nEnter the number of reward to claim (or 'cancel'): ").strip()
            if choice.lower() == "cancel":
                return

            reward_num = int(choice)
            if 1 <= reward_num <= len(available_rewards):
                reward_name = available_rewards[reward_num - 1]

                confirm = input(f"Are you sure you want to claim '{reward_name}'? (yes/no)").strip().lower()
                if confirm == 'yes':
                    if 'claimed' not in context.rewards[reward_name]:
                        context.rewards[reward_name] = {'tasks': context.rewards[reward_name], 'claimed': True}
    
                    self.save_and_load.save_rewards(context)
                    print(f"🎊 Congratulations! You've successfully claimed: {reward_name}!")
                    print("Enjoy your reward! 🎉")
                else:
                    print("Claim cancelled.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")

    def reward_delete(self, context):
        if not context.rewards:
            print("No rewards in your library yet.")
            return
        
        print("\n🔶 All your rewards until here:")
        only_rewards = list(context.rewards.keys())
        for index, reward in enumerate(only_rewards, start=1):
            print(f"{index}: {reward}")
            
        print("\n🔷 Enter the reward's number you wanna edit:")
        choice = input("> ").strip()
        
        if not choice.isdigit():
            print("Please enter a number.")
            return
        
        reward_number = int(choice)
        if not (1 <= reward_number <= len(only_rewards)):
            print("Number is not in the range.")
            return
        
        title = only_rewards[reward_number - 1]
        print(f"Selected reward: {title}")
        
        context.rewards.pop(title)
        self.save_and_load.save_rewards(context)
        print((f"Reward '{title}' deleted successfully. ☑️"))

def sync_rewards_with_tasks(context, save_and_load):
    updated = False

    for reward_name, tasks_dict in context.rewards.items():
        for task_name in tasks_dict.keys():
            if task_name in context.tasks:
                new_status = context.tasks[task_name]["status"] == "Completed"
                old_status = tasks_dict[task_name]

                if new_status != old_status:
                    tasks_dict[task_name] = new_status
                    updated = True
                    print(f"Updated task '{task_name}' status in reward '{reward_name}' to {new_status}")
    if updated:
        save_and_load.save_rewards(context)
        print("Rewards synchronized with tasks status.")   

    return updated

class Main:
    def __init__(self):
        self.context = Data_Context()
        self.save_and_load = Save_and_load()
        self.actions_for_tasks = Actions_Task(self.save_and_load)
        self.reward_section = Reward(self.save_and_load)

        self.save_and_load.load_rewards(self.context)
        self.save_and_load.load_tasks(self.context)
    
    def performing_program(self):
        print(("🗒️  Task Management System"))

        while True:
            print(("""\n               ✏️  Options:
                  1. Add a task 🫟
                  2. Update a task
                  3. Edit a task
                  4. Delete a task
                  5. View all tasks (To Do List) 📔
                  6. Rewards ✨
                  7. Quit"""))
            choice = input("\nEnter your choice (1-7) ").strip()

            if choice ==  "1":
                self.actions_for_tasks.add_task(self.context)
            elif choice == "2":
                self.actions_for_tasks.update_task_status(self.context)
            elif choice == "3":
                self.actions_for_tasks.edit_task(self.context)
            elif choice == "4":
                self.actions_for_tasks.delete(self.context)
            elif choice == "5":
                self.actions_for_tasks.show_all_tasks(self.context)
            elif choice == "6":
                self.reward_section.reward(self.context)
            elif choice == "7":
                print(("Fighting! 🔥"))
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = Main()
    app.performing_program()