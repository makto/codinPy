"""
The nth term of the sequence of triangle numbers is given by, tn=(1/2)*n*(n+); so the first ten triangle numbers are:
    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value.
For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.
Using words.txt, a 16K text file containing nearly two-thousand common English words, how many are triangle words?
"""

triangle_numbers = set()
n = 1
while True:
    nth = n*(n+1)/2
    if nth > 5000:      # produce enough triangle numbers, not all
        break
    triangle_numbers.add(nth)
    n += 1

def word_value(word):
    return sum([ord(letter)-64 for letter in word])

def is_triangle_word(word):
    return word_value(word) in triangle_numbers

raw_words = open('words.txt', 'r').read()
words = [word.strip('"') for word in raw_words.split(',')]
triangle_words = [word for word in words if is_triangle_word(word)]

print len(triangle_words)
