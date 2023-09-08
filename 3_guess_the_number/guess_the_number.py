import random

def get_int_input(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: Invalid input. Please enter an integer.")
        return None

def play_game(lives_remaining):
    number_to_guess = random.randrange(11)
    print(f"You have {lives_remaining} lives. Good luck!")
    
    while lives_remaining > 0:
        number = get_int_input("Type a number from 0 to 10: ")
        
        if number is None:
            continue

        if number == number_to_guess:
            print("You won!")
            return True
        
        lives_remaining -= 1
        print(f"Try again! You have {lives_remaining} lives remaining.")

    print("Sorry! You lose.")
    return False

def main():
    lives_remaining = 3
    play_game(lives_remaining)

if __name__ == "__main__":
    main()
