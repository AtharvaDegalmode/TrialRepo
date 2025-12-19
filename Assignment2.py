#Program to differentiate between positive,negative numbers and zero and even,odd integer.
while True:
        x = float(input("Enter a number: "))

        if x>0:
                print("It is Positive")
        elif x<0:
                print("It is Negative")
        else:
                print("Number is Zero")                
       
        if x%2==0:
                print("Number is Even")
        elif x%2==1:
                print("Number is Odd")
        else:
                print("Number is not Integer")        

    


   
