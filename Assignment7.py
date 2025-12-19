#Method 1
x="HelloPython"
vowels=["a","e","i","o","u","A","E","I","O","U"]
list=set(x)
num=0
for i in list:
    for j in vowels:
        if i==j:
             num=num+1
print("Number of vowels in given string is:",num)

#Method 2
x="HelloPython"
vowels1="aeiouAEIOU"
num1=0
for i in set(x):
    if i in vowels1:
        num1=num1+1
print("Number of Vowels in given string is:",num1)     

#Reversing a string
rstring=x[::-1]
print(rstring)

n=input("Enter any string:" )
r=n[::-1]
if n==r:
    print("The given string is a Palindrome")


