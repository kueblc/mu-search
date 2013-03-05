########################################################
# simhash.py
# Simple Hash Function
# Rory Thrasher
# MuSearch
# Web Science Spring 2013
#
# To use in your program:
# Place simhash.py in your program's directory.
# Place 'import simhash' at the top of your program.
# Call simhash.hash('string', 100), where the first item
# is your string, and the second item is the size of the
# table.  Simple hash will return an integer between 0
# and size-1 (inclusive).
########################################################

def hash(mystr, size):
    # Simple hash function to hash a string, based on Dan Bernstein's djb2
    # Input: mystr - a string that is to be hashed
    # Input: size - an integer (table size) for modular division
    hash = 3313 # arbitrary large prime number to initialize

    # Uses bitshifting to do the following algorithm:
    # hash(i) = hash(i-1) * 33 + str[i]
    # Bitshifting by 5 is the equivalent of multiplying hash by 32
    # Adding hash once means we can multiple hash by 33 very effeciently
    # We then add the ascii value of the next character
    for char in mystr:
        hash = ((hash << 5) + hash) + ord(char)

    # Output: hash - a integer between 0 and size-1 (inclusive)
    # Uses type long for mod as hash can get very large
    return int(long(hash)%long(size))
