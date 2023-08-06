import random


class RandoDraw:
    # ranges(int): sets the range for the guesser
    def __init__(self, ranges=10):
        self.ranges = ranges

    # generate random number and simply return to be used in the guessing function
    def generate_random(self):
        n = int(random.random() * self.ranges)
        return n

    """
    1. Calls the generate_random function and assign the returned variable to n
    2. Asks user for input a number between 0 and the decided range
    3. Checks the following conditions:
        - if number bigger than ranges variable or less than 0 it is out of range
        - if guess is bigger than n, print the guess is higher
        - if guess is smaller than n, print the guess is lower
        - else print Correct!
    """

    def cold_hot(self):
        n = self.generate_random()
        guess = input("Enter a random number between 0 and " + str(self.ranges))
        guess = int(guess)
        if guess > self.ranges or guess < 0:
            print("This number is out of range")
        elif guess > n:
            print("Number is higher than guess")
        elif guess < n:
            print("Number is lower than guess")
        else:
            print("Correct!")
