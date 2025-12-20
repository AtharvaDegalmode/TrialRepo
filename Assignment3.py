#Program to calculate sum of numbers upto an integer n using while and for loop 
# stop if a sentiel value is entered

m=int(input("enter an number: "))
sum1=0
for x in range(m+1):
   sum1=sum1+x 
print("Sum using for loop:",sum1)         
total = 0

total = 0

number = int(input("Enter a number (0 to stop): "))

while number != 0:
    total += number
    number = int(input("Enter a number (0 to stop): "))

print("The sum is:", total)



 
    


    






    