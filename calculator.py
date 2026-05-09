def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b


print("Simple Calculator")
print("-----------------")

while True:
    print("\nOperations: 1) Add  2) Subtract  3) Multiply  4) Divide  5) Quit")
    choice = input("Choose an operation (1-5): ")

    if choice == "5":
        print("Goodbye!")
        break

    if choice not in ("1", "2", "3", "4"):
        print("Invalid choice. Please enter a number between 1 and 5.")
        continue

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    if choice == "1":
        print(f"Result: {a} + {b} = {add(a, b)}")
    elif choice == "2":
        print(f"Result: {a} - {b} = {subtract(a, b)}")
    elif choice == "3":
        print(f"Result: {a} x {b} = {multiply(a, b)}")
    elif choice == "4":
        print(f"Result: {a} / {b} = {divide(a, b)}")
