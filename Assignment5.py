list=[1,2,2,3,4,4,4,5,6,7,8,8]
even_squares=[i*i for i in list if i%2==0]
print(even_squares)


list1=[1,"Ak47","apple","ball",3,9.5,False]
os_list=[i for i in list1 if type(i)==str]
print(os_list)