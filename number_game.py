import random

number = random.randint(1,10)
guess = None
while not guess == number: 
    guess = int( input("Guess a number from 1 to 10: ") )
    if guess < number:
        print("You guessed too low")
    elif guess > number:
        print("You guessed too high")
    else:
        print("You guessed correctly!")
    
