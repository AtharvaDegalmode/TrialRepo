x = float(input("Enter a number:" ))

    


   
if type(x)==float:
        if x % 2 == 0:
                print("The number is even")
        else:
                print("the number is odd")           
else:
    print("The number is not an integer, so it can't be even or odd.")


    
if x > 0:
        print("The number is positive.")
elif x < 0:
        print("The number is negative.")
else:
        print("The number is zero.")

   
