#This program generates a password
#And saves it both to the clipboard and a separate file
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
        'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)

    #Automaticall paste the password to the clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
#When user clicks the Add button
#Save the website, username, and password to a data.txt file
#Ex. Amazon| Email | Password using a function
def save():
    #Get the entered data
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    #Error message if no data entered and Add button pressed:
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Stop!", message="You must enter data in all the fields!")
    else:
        try:
            #use "r" when reading to the file:
            with open("data.json", "r") as data_file:
            #Now read data from it:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)

        finally:
            #Delete the data in the website and password blanks
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
#This is triggered when the Search button is pressed
def find_password():
    website = website_entry.get()
    try:
    #read the json file to find the website name
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # If the website name key is not in the JSON file:
        # Messagebox that reads "No details for website exists"
        messagebox.showinfo(title="Data Not Found", message="No data.")
    else:
        # Now read data from it, looking for the key of the website name:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            #If the key of the website name is found, give the website, email,
            #and password values in the messagebox
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Data Not Found", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
#Opens a window
window = Tk()
window.title("Password Manager")
#Padding
window.config(padx=40, pady=40)

#Using Canvas to upload a picture, Row 0, Column 1
canvas = Canvas(width=225, height=225)
logo_img = PhotoImage(file=r".\logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1,row=0)

#Now we need 3 entry boxes for the website, username, and password
#Covering 2 columns, except the password

#Website Section Row 1
#Label
website_label = Label(text="Website:")
website_label.grid(column=0,row=1)
#Start the cursor in the box
website_label.focus()

#Website Entry
website_entry = Entry(width=21)
#Gets text in entry
#print(entry.get())
website_entry.grid(column=1, row=1)

#Email/Username Section Width 35 Row 3 columnspan 2
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

#Email/Username Entry
email_entry = Entry(width=35)
email_entry.insert(0, "useremail@something.com")
email_entry.grid(column=1, row=2, columnspan=2)

#Password Section Width 21 Column 0 Row 3
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Password Entry
password_entry = Entry(width=17)
password_entry.grid(column=1, row=3)

#Search button; pops up a box with the emain and password for that website
search_button = Button(text="Search", width= 13, command=find_password)
search_button.grid(column=2, row=1)

#Generate Password button  Column 2 Row 3
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

#Add button Width 36  Row 4 Column 1 Columnspan 2
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)


#listens to what user will do
#Goes at the end of the program
window.mainloop()