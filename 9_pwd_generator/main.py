import random
import string

def generate_password(length=12, exclude_chars=''):
    # Character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    punctuation = ''.join(ch for ch in string.punctuation if ch not in exclude_chars)

    # Ensure at least one character from each type
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(punctuation)
    ]

    # Fill the rest of the password
    for _ in range(length - 4):
        password.append(random.choice(uppercase_letters + lowercase_letters + digits + punctuation))

    random.shuffle(password)
    return ''.join(password)

def validate_password(password):
    if any(ch.isupper() for ch in password) and \
       any(ch.islower() for ch in password) and \
       any(ch.isdigit() for ch in password) and \
       any(ch in string.punctuation for ch in password):
        return True
    return False

if __name__ == "__main__":
    exclude_chars = '"\'\\/'
    try:
        length = int(input("Enter the desired password length (minimum 4): "))
        if length < 4:
            print("Length is too short. Setting length to 4.")
            length = 4
        num_passwords = int(input("Enter the number of passwords to generate: "))
        
        for _ in range(num_passwords):
            password = generate_password(length, exclude_chars)
            print(f"{_}. Generated Password: {password} (Valid: {validate_password(password)})")
            

    except ValueError:
        print("Please enter a valid number.")
