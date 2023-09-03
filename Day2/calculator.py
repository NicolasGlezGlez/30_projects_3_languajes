def perform_operation(op, num1, num2):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            return "Error: Division by zero"
        else:
            return num1 / num2
    else:
        return "Error: Invalid operator"

def get_float_input(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        return "Error: Invalid input"

def main():
    while True:
        num1 = get_float_input("Enter a number: ")
        op = input("Enter an operator (+,-,*,/): ")
        num2 = get_float_input("Enter another number: ")

        if isinstance(num1, str) or isinstance(num2, str):
            print("Error: Invalid input. Please enter numbers.")
            continue

        result = perform_operation(op, num1, num2)

        print(f"Result: {result}")

        another = input("Would you like to perform another operation? (y/n): ")
        if another.lower() != 'y':
            break

if __name__ == "__main__":
    main()
