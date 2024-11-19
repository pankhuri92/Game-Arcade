import random

def load_words(file_path):
    """Load and return a list of 4-letter words from the provided file."""
    return [line.strip() for line in open(file_path)]

def filter_words(words, guess, cows, bulls):
    """Filter words based on cows and bulls feedback."""
    def match_cows_bulls(word):
        common = sum(min(guess.count(c), word.count(c)) for c in set(guess))
        match = sum(g == w for g, w in zip(guess, word))
        return match == bulls and (common - match) == cows

    return [word for word in words if match_cows_bulls(word)]

def play_cows_and_bulls(file_path):
    words = load_words(file_path)
    best_starts = ['acre', 'pain', 'riot', 'mile', 'quit']

    print("Let's play Cows and Bulls!")
    print("Think of a 4-letter word, and I'll try to guess it.")
    print("You'll need to tell me how many bulls (correct letter in the correct position) I get for each guess.")
    print("If there are cows (correct letter in the wrong position), you'll tell me that too, unless all 4 are bulls!")

    attempts = 0
    while words:
        if best_starts:
            guess = best_starts.pop(0)
        else:
            guess = random.choice(words)

        print(f"My guess is: {guess}")
        bulls = int(input("Bulls: "))

        if bulls == 4:
            print(f"I guessed the word '{guess}' in {attempts + 1} tries!")
            break

        cows = int(input("Cows: "))
        attempts += 1

        words = filter_words(words, guess, cows, bulls)
        if not words:
            print("Seems like there's been some confusion. Let's try again.")
            break

play_cows_and_bulls("four_letter_words.txt")