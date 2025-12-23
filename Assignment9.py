#Function with positional arguments
def add(a, b):
    return a + b
#Function with default argument
def greet(name, msg="How Are You"):
    return msg, name
#Function with variable number of arguments
def total(list_numbers):
    return sum(list_numbers)
#Function returning multiple values
def operations(x, y):
    return x + y, x - y, x * y
# Calling Function  
print("Summation:",add(3, 4))                     
print("Greetings:",(greet("Atharva")))            
print("Total:",total([1, 2, 3, 4]))             
x,y,z = operations(10, 5)          
print("add,subtract,multipy:",x,y,z)
