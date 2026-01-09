from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','fields can not be empty')
    elif usernameEntry.get()=='bhuvan.k.k' and passwordEntry.get()=='1234':
        messagebox.showinfo('Success','welcome')
        window.destroy()
        import sms 

    else:
        messagebox.showerror('Error','enter correct details')   


window = Tk()
window.title("Bank employee Attendance - Login")
window.geometry('1280x700+0+0')
window.resizable(False, False)

# --- Background Image ---
bgimage = ImageTk.PhotoImage(file='bg.jpg')
bglabel = Label(window, image=bgimage)
bglabel.place(x=0, y=0)

# --- Login Frame ---
loginFrame = Frame(window, bg='white', bd=2, relief=RIDGE)
loginFrame.place(x=450, y=200, width=400, height=350)

# --- Logo Image ---
original_logo = Image.open('ip1.png')
resized_logo = original_logo.resize((80, 80))  # smaller for better aesthetics
logoImage = ImageTk.PhotoImage(resized_logo)
logoLabel = Label(loginFrame, image=logoImage, bg='white')
logoLabel.grid(row=0, column=0, columnspan=2, pady=20)

# --- Username Label and Entry ---
usernameLabel = Label(loginFrame, text='Username:', font=('Helvetica', 14, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, padx=10, pady=10, sticky='w')
usernameEntry = Entry(loginFrame, font=('Helvetica', 12), bd=2, relief=GROOVE,fg='royalblue')
usernameEntry.grid(row=1, column=1, padx=10, pady=10)

# --- Password Label and Entry ---
passwordLabel = Label(loginFrame, text='Password:', font=('Helvetica', 14, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, padx=10, pady=10, sticky='w')
passwordEntry = Entry(loginFrame, font=('Helvetica', 12), bd=2, relief=GROOVE, show='@')
passwordEntry.grid(row=2, column=1, padx=10, pady=10)

# --- Login Button ---
loginButton = Button(
    loginFrame,
    text='Login',
    font=('Helvetica', 14, 'bold'),
    bg='#4CAF50',
    fg='white',
    cursor='hand2',
    width=15,
    command=login  # <<< this connects the button to your login function
)
loginButton.grid(row=3, column=0, columnspan=2, pady=20)


window.mainloop()
