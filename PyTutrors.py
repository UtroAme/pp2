#print("Hello, World!")


#Check Version
import sys
print(sys.version)


#Python Indentation
if 5 > 2:
  print("Five is greater than two!")


if 5 > 2:
 print("Five is greater than two!") 
if 5 > 2:
        print("Five is greater than two!") #use indentation to indicate a block of code.

#Python Variables
x = 5
y = "Hello, World!" #There is no command for declaring a var

#This is a comment
#Multiline Comments
'''
This is a comment
written in
more than just one line
'''

#Creating Variables
x = 5       #x is of type int
y = "John"  #y is of type str
print(x)
print(y)

x = str(3)   # x will be '3'
y = int(3)   # y will be 3
z = float(3) # z will be 3.0

#Get the type
print(type(x)) # from last we will get str

a = 4
A = "Sally" #A will not overwrite a

#Variable Names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#illegal Variable names:
'''2myvar = "John"
my-var = "John"
my var = "John" '''

#Multi Words Variable Names
myVariableName = "John"   #Camel case
MyVariableName = "John"   #Pascal Case
my_variable_name = "John" #Snake Case

#Many Values to Multiple Variables
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z) 

#One Value to Multiple Variables
x = y = z = "Orange"
print(x)
print(y)
print(z) 

#Unpack a Collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#Output Variables {use print()}
x = "Python"
y = "is"
z = "awesome"
print(x, y, z) #separated by a comma

x = "Python "
y = "is "
z = "awesome"
print(x + y + z) # There is a whitespace int end of x & y

x = 5
y = 10
print(x + y) #int + int, if is int + str = Error

x = 5
y = "John"
print(x, y) # in there we can use int, str

#Global Variables
#Create a variable outside of a function, and use it inside the function
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()  

#Create a variable inside a function, with the same name as the global variable
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

#If you use the global keyword, the variable belongs to the global scope:
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

#To change the value of a global variable inside a function, refer to the variable by using the global keyword:
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

#Python Data types in there https://www.w3schools.com/python/python_datatypes.asp

#Python Numbers
x = 1    # int
y = 2.8  # float
z = 1j   # complex

#Integers:
x = 1
y = 35656222554887711 #dont have a lenght
z = -3255522          #can be negative

#Floats:
x = 1.10
y = 1.0    #containing one or more decimals
z = -35.59 #positive or negative
f = 35e3
r = 12E4
s = -87.7e100  #Float can also be scientific numbers with an "e" to indicate the power of 10.

#Complex:
x = 3+5j
y = 5j
z = -5j #a "j" as the imaginary part

#Convert from one type to another:
x = 1    # int
y = 2.8  # float
z = 1j   # complex

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex: !u cant convert complex into another num type
c = complex(x)

#Import the random module, and display a random number between 1 and 9:
import random
print(random.randrange(1, 10)) #10 is not included

#Specify a Variable Type
'''
int() - can be float, str
float() - can be str, int
str() - 
'''

#Integers:
x = int(1)   # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3

#Floats:
x = float(1)     # x will be 1.0
y = float(2.8)   # y will be 2.8
z = float("3")   # z will be 3.0
w = float("4.2") # w will be 4.2

#Strings:
x = str("s1") # x will be 's1'
y = str(2)    # y will be '2'
z = str(3.0)  # z will be '3.0'

'''Python String'''
# 'hello' is the same as "hello"

'''Quotes Inside Quotes'''
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"') #they don't match

#You can use three double quotes for Multiline Strings:
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a) #also can be used with ''' three single quotes

#Strings are Arrays
a = "Hello, World!"
print(a[1])

#Loop through the letters in the word "banana":
for x in "banana":
  print(x)
'''
that give us:
b
a
n
a
n
a
'''

#The len() function returns the length of a string:
a = "Hello, World!"
print(len(a))

#Check if "free" is present in the following text:
txt = "The best things in life are free!"
print("free" in txt)

#Print only if "free" is present:
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

#Check if "expensive" is NOT present in the following text:
txt = "The best things in life are free!"
print("expensive" not in txt)

#print only if "expensive" is NOT present:
txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")

'''Slicing'''
#Get the characters from position 2 to position 5 (not included):
b = "Hello, World!"
print(b[2:5])

#Get the characters from the start to position 5 (not included):
b = "Hello, World!"
print(b[:5])

#Get the characters from position 2, and all the way to the end:
b = "Hello, World!"
print(b[2:])

#Get the characters:
#From: "o" in "World!" (position -5)
#To, but not included: "d" in "World!" (position -2):
b = "Hello, World!"
print(b[-5:-2])

'''Modify Strings'''
#The upper() method returns the string in upper case:
a = "Hello, World!"
print(a.upper())

#The lower() method returns the string in lower case:
a = "Hello, World!"
print(a.lower())

#The strip() method removes any whitespace from the beginning or the end:
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#The replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J"))

#The split() method splits the string into substrings if it finds instances of the separator:
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

'''String Concatenation'''
#Merge variable a with variable b into variable c:
a = "Hello"
b = "World"
c = a + b
print(c)

#To add a space between them, add a " ":
a = "Hello"
b = "World"
c = a + " " + b
print(c)

''' Format - Strings'''
#how we know we cant str + int, so use f-string
#Create an f-string:
age = 36
txt = f"My name is John, I am {age}" #put f in front and add {int case}
print(txt)

#Display the price with 2 decimals:
price = 59
txt = f"The price is {price:.2f} dollars" #we will get "The price is 59.00 dollars"
print(txt)

#Perform a math operation in the placeholder, and return the result:
txt = f"The price is {20 * 59} dollars"
print(txt)

'''Escape Characters'''
txt = "We are the so-called \"Vikings\" from the north." # \" use this for "

'''
Other escape characters used in Python:
Code |	Result	
\'	 | Single Quote	
\\	 | Backslash	
\n	 | New Line	
\r	 | Carriage Return	
\t	 | Tab	
\b	 | Backspace	
\f	 | Form Feed	
\ooo | Octal value	
\xhh | Hex value
'''

#also we have string methods
#All string methods return new values. They do not change the original string.