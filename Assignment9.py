#Function with positional arguments
def add(a, b):
    return a + b


#Function with default argument
def greet(name, msg="Hello"):
    return msg, name


#Function with variable number of arguments
def total(*numbers):
    return sum(numbers)


#Function returning multiple values
def operations(x, y):
    return x + y, x - y, x * y


# Calling Function  
print(add(3, 4))                     # positional
print(greet("Atharva"))              # default
print(total(1, 2, 3, 4))             # variable args

s, d, m = operations(10, 5)           # multiple return values
print(s, d, m)
