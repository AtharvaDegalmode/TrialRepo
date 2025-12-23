contacts ={"name":"phone_number",}  # Dictionary to store contacts


def add_contact():
    name = input("Enter contact name: ")
    phone_number = input("Enter phone number: ")
    if len(str(phone_number))==10:
      contacts[name] = phone_number
      print("Contact added successfully!\n")
    else:
       print("Invalid Number")  
def clear_contacts():
   contacts.clear()
def display_contacts():
   print(contacts)
display_contacts()
   
   