import json
import os

# The file where your tasks will be saved on disk
SAVE_FILE = os.path.expanduser("~/projects/todo_tasks.json")


def load_tasks():
    """Load tasks from the save file. Returns an empty list if no file exists yet."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save the current list of tasks to the save file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def show_tasks(tasks):
    """Print all tasks with a number next to each one."""
    if not tasks:
        print("\n  (No tasks yet! Add one.)\n")
    else:
        print("\n--- Your To-Do List ---")
        for i, task in enumerate(tasks, start=1):
            # Show a checkmark for done tasks, empty box for pending
            status = "[x]" if task["done"] else "[ ]"
            print(f"  {i}. {status} {task['name']}")
        print("-----------------------\n")


def add_task(tasks):
    """Ask the user for a task name and add it to the list."""
    name = input("Enter task name: ").strip()
    if name:
        tasks.append({"name": name, "done": False})
        save_tasks(tasks)
        print(f'  Task "{name}" added!\n')
    else:
        print("  No task name entered. Try again.\n")


def mark_done(tasks):
    """Let the user pick a task number to mark as complete."""
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to mark as done: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            save_tasks(tasks)
            print(f'  Task "{tasks[num - 1]["name"]}" marked as done!\n')
        else:
            print("  Invalid number. Try again.\n")
    except ValueError:
        print("  Please enter a valid number.\n")


def delete_task(tasks):
    """Let the user pick a task number to delete it from the list."""
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f'  Task "{removed["name"]}" deleted!\n')
        else:
            print("  Invalid number. Try again.\n")
    except ValueError:
        print("  Please enter a valid number.\n")


def main():
    """Main loop — keeps the app running until the user chooses to quit."""
    print("============================")
    print("   Welcome to To-Do List!   ")
    print("============================")

    # Load any previously saved tasks when the app starts
    tasks = load_tasks()

    while True:
        print("What would you like to do?")
        print("  1. Show all tasks")
        print("  2. Add a new task")
        print("  3. Mark a task as done")
        print("  4. Delete a task")
        print("  5. Quit")

        choice = input("Enter a number (1-5): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("\n  Goodbye! Your tasks are saved.\n")
            break
        else:
            print("  Please enter a number between 1 and 5.\n")


# This makes sure main() only runs when you run this file directly
if __name__ == "__main__":
    main()
