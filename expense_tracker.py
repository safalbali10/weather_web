"""
Expense Tracker — saves expenses to a JSON file so they survive closing.
Each expense is stored as: {"name": "...", "amount": 12.50}
"""

import json
import os

# File where expenses are saved between sessions
SAVE_FILE = os.path.expanduser("~/projects/expenses.json")


def load_expenses():
    """Load expenses from the JSON file. Returns an empty list if the file doesn't exist yet."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    """Save the current list of expenses to the JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def show_expenses(expenses):
    """Print all expenses with an index number, name, and amount."""
    if not expenses:
        print("\n  No expenses yet.")
        return
    print("\n  #   Name                      Amount")
    print("  " + "-" * 40)
    for i, expense in enumerate(expenses, start=1):
        # Left-align the name in a 26-char wide column, right-align the amount
        print(f"  {i:<3} {expense['name']:<26} ₹{expense['amount']:.2f}")


def show_total(expenses):
    """Calculate and print the total amount spent across all expenses."""
    total = sum(expense["amount"] for expense in expenses)
    print(f"\n  Total spent: ₹{total:.2f}")


def add_expense(expenses):
    """Ask the user for a name and amount, then add the expense to the list."""
    name = input("\n  Expense name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return

    # Keep asking until the user enters a valid positive number
    while True:
        amount_str = input("  Amount (₹): ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("  Amount must be greater than zero.")
            else:
                break
        except ValueError:
            print("  Please enter a valid number (e.g. 250.00).")

    expenses.append({"name": name, "amount": amount})
    save_expenses(expenses)
    print(f"  Added: {name} — ₹{amount:.2f}")


def delete_expense(expenses):
    """Show all expenses and let the user pick one to delete by number."""
    if not expenses:
        print("\n  No expenses to delete.")
        return

    show_expenses(expenses)
    while True:
        choice = input("\n  Enter the # to delete (or 0 to cancel): ").strip()
        try:
            index = int(choice)
            if index == 0:
                return
            if 1 <= index <= len(expenses):
                removed = expenses.pop(index - 1)
                save_expenses(expenses)
                print(f"  Deleted: {removed['name']} — ₹{removed['amount']:.2f}")
                return
            else:
                print(f"  Please enter a number between 1 and {len(expenses)}.")
        except ValueError:
            print("  Please enter a valid number.")


def print_menu():
    """Print the main menu options."""
    print("\n========== Expense Tracker ==========")
    print("  1. Add an expense")
    print("  2. View all expenses")
    print("  3. View total spent")
    print("  4. Delete an expense")
    print("  5. Quit")
    print("=====================================")


def main():
    """Main loop — shows the menu and handles the user's choice until they quit."""
    expenses = load_expenses()
    print(f"\nLoaded {len(expenses)} expense(s) from file.")

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("\nGoodbye! Your expenses are saved.\n")
            break
        else:
            print("  Invalid choice. Please enter a number from 1 to 5.")


# Run the app
if __name__ == "__main__":
    main()
