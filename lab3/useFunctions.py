from functions import guess
import random

print("Hello! What is ypur name?")
name = input()
print(name)
print(f"Well, {name}, I am thinking of a number beetween 1 and 20.")
randomNum = random.randint(1,20)
print("Take a guess.")
num = int(input())
guess(num, randomNum)