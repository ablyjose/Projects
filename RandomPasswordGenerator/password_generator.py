# This is a random password generator
# The goal is to:
# Output parameter options with selections available
# Create a password based on parameters
# Create a unique password every time
# Toss the passwords into a "database"

import secrets
from random import shuffle
import string

website_name = input("What website are you creating a password for? ")

length = int(input("What is the desired length of your password? We suggest between 12-24 characters long: "))

char = string.ascii_letters + string.digits
specials = string.punctuation.replace(',', '|')

# lower_letters = []
# upper_letters = []
# nums = []
# specials = []

lowercase = int(input("How many lowercase letters are required? "))
# for l in range(lowercase):
#     lower_letters.append(secrets.choice(string.ascii_lowercase))

uppercase = int(input("How many uppercase letters are required? "))
# for u in range(uppercase):
    # upper_letters.append(secrets.choice(string.ascii_uppercase))

numbers = int(input("How many numbers are required? "))
# for n in range(numbers):
#     nums.append(secrets.choice(string.digits))

special = int(input("How many special symbols are required? "))
# for s in range(special):
#     specials.append(secrets.choice(string.punctuation.replace(',', '|')))

# if (len(lower_letters) + len(upper_letters) + len(nums) + len(specials)) > length:
#     length = len(lower_letters) + len(upper_letters) + len(nums) + len(specials)

lo = 0
up = 0
di = 0

while True:
    password = ''.join(secrets.choice(char) for i in range(length - special))
    password.join(secrets.choice(specials) for i in range(special))

    for letter in password:
        if letter.islower():
            lo+=1
        elif letter.isupper():
            up+=1
        elif letter.isdigit():
            di+=1

    if (lo >= lowercase) and (up >= uppercase) and (di >= numbers):
        break

""" prelim = "".join(lower_letters + upper_letters + nums + specials)
listed = list(prelim)

shuffle(listed)
password = "".join(listed) """

with open("RandomPasswordGenerator/passwords.csv", "a") as f:
    f.write(website_name + "," + password + "\n")

print()
print("Password saved to secure database")

char = string.ascii_letters + string.digits
specials = string.punctuation.replace(',', '')
