import random

points = 0
while True:
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)

    print("You have a %s and a %s" % (dice1,dice2))
    total = dice1 + dice2
    print("Your total is %s" % total)
    while total <= 25:
        response = input("Do you want to roll again? ")
        if response == "no":
            break
        else:
            dice1 = random.randint(1,6)
            total = total + dice1
            print("Your new total is %s" % total)
    if total > 25:
        print("You went too high - no points")
    elif total == 25:
        print("You got 10 points!")
        points = points + 10
    elif total >= 20 and total < 25:
        print("You got 7 points")
        points = points + 7
    print("You have %s points" % points)
