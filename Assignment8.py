#Defining functon for average of list as avg_list
def avg_list(list):
    num=sum(list)
    avg=num/len(list)
    print("The average of elements in given list is: ",avg)    
set=[1,2,3,4,5,9] 

def rev_string(x):
    t=x[::-1]
    print(t)

#calling out function to calculate average of numbers in list:set
avg_list(set)
rev_string("Poha")