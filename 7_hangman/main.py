import requests
import random

def fetch_word():
    response = requests.get("https://api.datamuse.com/words?rel_rhy=cat")
    words = response.json()
    return random.choice(words)["word"]

def play_hangman():
    word = fetch_word()
    word_underscores = '_' * len(word)
    attempts = 6
    guessed_letters = []

    print("Welcome to the Hangman game!")
    while attempts > 0 and '_' in word_underscores:
        print(word_underscores)
        print(f"Remaining attempts: {attempts}")
        print(f"Guessed letters: {', '.join(guessed_letters)}")

        letter = input("Guess a letter: ").lower()

        if letter in guessed_letters:
            print("You've already guessed that letter. Try another one.")
            continue

        if letter in word:
            for index, char in enumerate(word):
                if char == letter:
                    word_underscores = word_underscores[:index] + letter + word_underscores[index+1:]
        else:
            attempts -= 1

        guessed_letters.append(letter)

    if '_' not in word_underscores:
        print(f"You won! The word was {word}.")
    else:
        print(f"You lost. The word was {word}.")

play_hangman()
