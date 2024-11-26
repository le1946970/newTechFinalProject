import random

# This python scripts generates a 10 digit long random number.
# The chances of getting the same number twice are very slim.

class RNG():
    # Normally, I would use a singleton when using random number generators,
    # but since I can't really make the constructor private in python I don't know how.

    # generates a random number of a specific number of digits
    def generate(self, digits):
        digits = self.get_number_to_multiply(digits)
        # generate a random number between 0 and 1
        rand = random.random()

        # make that number 10 digits long and return it.
        return int(rand * digits)
    
    # generates the number that the random number needs to be multiplied to in order to have the right amount of digits
    def get_number_to_multiply(self, number):
        # creates a string with the character '1'
        str_number = '1'

        # add the specific number of '0' char to the end of the string
        for i in range(number):
            str_number += '0'

        # return the string turned into an integer
        return int(str_number)