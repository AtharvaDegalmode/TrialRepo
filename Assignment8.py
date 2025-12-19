#Defining functon for average of list as avg_list
def avg_list(list):
    num=sum(list)
    avg=num/len(list)
    print("The average of elements in given list is: ",avg)    
set=[1,2,3,4,5,9] 
#calling out function to calculate average of numbers in list:set
avg_list(set)   