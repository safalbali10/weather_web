"""
Password Generator App
======================
Generates strong passwords based on your preferences.
You can pick length, character types, choose a favourite,
and save it to a file.
"""

import random
import string
import os

# The file where saved passwords will be stored
SAVE_FILE = os.path.expanduser("~/projects/saved_passwords.txt")


def get_yes_no(prompt):
    """
    Asks the user a yes/no question and returns True for yes, False for no.
    Keeps asking until a valid answer is given.
    """
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("  Please enter 'y' for yes or 'n' for no.")


def get_password_length():
    """
    Asks the user for a password length between 6 and 128.
    Keeps asking until a valid number is entered.
    """
    while True:
        try:
            length = int(input("How long should each password be? (6–128): ").strip())
            if 6 <= length <= 128:
                return length
            else:
                print("  Please enter a number between 6 and 128.")
        except ValueError:
            print("  That's not a valid number. Please try again.")


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """
    Builds the set of characters to use when generating passwords.
    Returns a string containing all allowed characters.

    Parameters:
        use_upper   – include A–Z
        use_lower   – include a–z
        use_digits  – include 0–9
        use_symbols – include !@#$% etc.
    """
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase   # A–Z
    if use_lower:
        pool += string.ascii_lowercase   # a–z
    if use_digits:
        pool += string.digits            # 0–9
    if use_symbols:
        pool += string.punctuation       # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

    return pool


def generate_password(length, pool):
    """
    Generates a single random password of the given length
    using characters from the provided pool.
    Uses random.SystemRandom for cryptographically stronger randomness.
    """
    rng = random.SystemRandom()
    return "".join(rng.choice(pool) for _ in range(length))


def generate_five_passwords(length, pool):
    """
    Generates and returns a list of 5 different passwords.
    """
    passwords = []
    for _ in range(5):
        passwords.append(generate_password(length, pool))
    return passwords


def display_passwords(passwords):
    """
    Prints the list of passwords numbered 1–5.
    """
    print("\n  Here are your 5 password options:")
    print("  " + "-" * 40)
    for i, pw in enumerate(passwords, start=1):
        print(f"  {i}. {pw}")
    print("  " + "-" * 40)


def pick_favourite(passwords):
    """
    Asks the user to pick one of the 5 passwords as their favourite.
    Returns the chosen password string.
    """
    while True:
        try:
            choice = int(input("\n  Enter the number of your favourite (1–5): ").strip())
            if 1 <= choice <= 5:
                return passwords[choice - 1]
            else:
                print("  Please enter a number between 1 and 5.")
        except ValueError:
            print("  That's not a valid number. Please try again.")


def save_password(password):
    """
    Appends the chosen password to the save file (one password per line).
    Creates the file if it doesn't exist yet.
    """
    with open(SAVE_FILE, "a") as f:
        f.write(password + "\n")
    print(f"\n  Password saved to: {SAVE_FILE}")


def show_saved_passwords():
    """
    Reads and displays all passwords previously saved to the file.
    Shows a message if no passwords have been saved yet.
    """
    if not os.path.exists(SAVE_FILE):
        print("\n  No saved passwords yet.")
        return

    with open(SAVE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("\n  No saved passwords yet.")
    else:
        print(f"\n  Saved passwords ({len(lines)} total):")
        print("  " + "-" * 40)
        for i, pw in enumerate(lines, start=1):
            print(f"  {i}. {pw}")
        print("  " + "-" * 40)


def main():
    """
    Main loop of the app.
    Shows the menu, handles the user's choice, and repeats until they quit.
    """
    print("=" * 50)
    print("       Welcome to the Password Generator!")
    print("=" * 50)

    while True:
        # --- Main menu ---
        print("\nWhat would you like to do?")
        print("  1. Generate new passwords")
        print("  2. View saved passwords")
        print("  3. Quit")

        menu_choice = input("\nEnter 1, 2, or 3: ").strip()

        # --- Option 3: Quit ---
        if menu_choice == "3":
            print("\nGoodbye! Stay secure. :)\n")
            break

        # --- Option 2: View saved passwords ---
        elif menu_choice == "2":
            show_saved_passwords()

        # --- Option 1: Generate passwords ---
        elif menu_choice == "1":

            # Step 1: Ask for password length
            print()
            length = get_password_length()

            # Step 2: Ask which character types to include
            print("\nWhich character types do you want to include?")
            use_upper   = get_yes_no("  Uppercase letters (A–Z)?")
            use_lower   = get_yes_no("  Lowercase letters (a–z)?")
            use_digits  = get_yes_no("  Numbers (0–9)?")
            use_symbols = get_yes_no("  Symbols (!@#$%...)?")

            # Build the character pool from the chosen options
            pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

            # Make sure at least one type was chosen
            if not pool:
                print("\n  You must select at least one character type. Please try again.")
                continue

            # Step 3: Generate and display 5 passwords
            passwords = generate_five_passwords(length, pool)
            display_passwords(passwords)

            # Step 4: Ask if they want to save a favourite
            if get_yes_no("\nWould you like to save one of these passwords?"):
                favourite = pick_favourite(passwords)
                save_password(favourite)
                print(f"\n  Your saved password: {favourite}")

        else:
            print("\n  Invalid choice. Please enter 1, 2, or 3.")


# Only run main() when this file is executed directly (not imported)
if __name__ == "__main__":
    main()
