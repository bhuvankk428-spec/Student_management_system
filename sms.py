from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox
import pymysql

import pandas as pd
from tkinter import filedialog, messagebox
import winsound  

def iexit():
    s=messagebox.askyesno('confirm','are you sure you want to exit')
    if s:
        root.destroy()
    else:
        pass    


def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or mobileEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=add_window)
        else:
            try:
                query = 'INSERT INTO student(id, name, mobile, email, address, gender, dob, addedtime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
                current_time = time.strftime('%H:%M:%S')
                current_date = time.strftime('%d/%m/%Y')
                added_time = current_date + "   " + current_time
                mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), added_time))
                con.commit()
                # After inserting into database
                mycursor.execute('SELECT * FROM student')
                fetch_data = mycursor.fetchall()
                studentTable.delete(*studentTable.get_children())  # clear the table first
                for data in fetch_data:
                     studentTable.insert('', END, values=data)
                messagebox.showinfo('Success', 'Bank employee Added Successfully', parent=add_window)
                add_window.destroy()
                winsound.Beep(1000, 1000) 
            except Exception as e:
                messagebox.showerror('Error', f'Something went wrong\n{str(e)}', parent=add_window)
                winsound.Beep(1000, 1000) 
                
    # --- Add Student Window ---
    add_window = Toplevel()
    add_window.title('Add employee')
    add_window.grab_set()
    add_window.geometry('470x470+220+200')
    add_window.resizable(False, False)

    # --- Labels and Entry Fields ---
    idLabel = Label(add_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    idEntry = Entry(add_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, padx=20, pady=10)

    nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    nameEntry = Entry(add_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, padx=20, pady=10)

    mobileLabel = Label(add_window, text='Mobile No', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    mobileEntry = Entry(add_window, font=('roman', 15, 'bold'))
    mobileEntry.grid(row=2, column=1, padx=20, pady=10)

    emailLabel = Label(add_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    emailEntry = Entry(add_window, font=('roman', 15, 'bold'))
    emailEntry.grid(row=3, column=1, padx=20, pady=10)

    addressLabel = Label(add_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=10, sticky='w')
    addressEntry = Entry(add_window, font=('roman', 15, 'bold'))
    addressEntry.grid(row=4, column=1, padx=20, pady=10)

    genderLabel = Label(add_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=10, sticky='w')
    genderEntry = Entry(add_window, font=('roman', 15, 'bold'))
    genderEntry.grid(row=5, column=1, padx=20, pady=10)

    dobLabel = Label(add_window, text='D.O.B.', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=10, sticky='w')
    dobEntry = Entry(add_window, font=('roman', 15, 'bold'))
    dobEntry.grid(row=6, column=1, padx=20, pady=10)

    # --- Submit Button ---
    submitButton = ttk.Button(add_window, text='Submit', command=add_data)
    submitButton.grid(row=7, columnspan=2, pady=20)


def search_student():
    def search_data():
        query = 'SELECT * FROM student WHERE id=%s OR name=%s '
        mycursor.execute(query, (idEntry.get(), nameEntry.get()))
        rows = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for row in rows:
            studentTable.insert('', END, values=row)
        search_window.destroy()    
        winsound.Beep(5000, 500) 
    search_window = Toplevel()
    search_window.title('Search employee')
    search_window.geometry('470x300+220+200')
    search_window.resizable(False, False)

    idLabel = Label(search_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    idEntry = Entry(search_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, padx=20, pady=10)

    nameLabel = Label(search_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    nameEntry = Entry(search_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, padx=20, pady=10)

    searchButton = ttk.Button(search_window, text='Search', command=search_data)
    searchButton.grid(row=4, columnspan=2, pady=20)

     
def delete_student():
    selected_item = studentTable.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a employee to delete')
        return
    data = studentTable.item(selected_item)['values']
    id_to_delete = data[0]
    query = 'DELETE FROM student WHERE id=%s'
    mycursor.execute(query, (id_to_delete))
    con.commit()
    studentTable.delete(selected_item)
    messagebox.showinfo('Success', 'employee deleted successfully')


def update_student():
    def update_data():
        query = 'UPDATE student SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s WHERE id=%s'
        mycursor.execute(query, (nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), idEntry.get()))
        con.commit()
        messagebox.showinfo('Success', 'employee Updated Successfully', parent=update_window)
        update_window.destroy()
        show_student()

    selected_item = studentTable.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a employee to update')
        return
    data = studentTable.item(selected_item)['values']

    update_window = Toplevel()
    update_window.title('Update Bank employee')
    update_window.geometry('470x470+220+200')
    update_window.resizable(False, False)

    idLabel = Label(update_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    idEntry = Entry(update_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, padx=20, pady=10)
    idEntry.insert(0, data[0])
    idEntry.config(state='readonly')

    nameLabel = Label(update_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    nameEntry = Entry(update_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, padx=20, pady=10)
    nameEntry.insert(0, data[1])

    mobileLabel = Label(update_window, text='Mobile No', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    mobileEntry = Entry(update_window, font=('roman', 15, 'bold'))
    mobileEntry.grid(row=2, column=1, padx=20, pady=10)
    mobileEntry.insert(0, data[2])

    emailLabel = Label(update_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    emailEntry = Entry(update_window, font=('roman', 15, 'bold'))
    emailEntry.grid(row=3, column=1, padx=20, pady=10)
    emailEntry.insert(0, data[3])

    addressLabel = Label(update_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=10, sticky='w')
    addressEntry = Entry(update_window, font=('roman', 15, 'bold'))
    addressEntry.grid(row=4, column=1, padx=20, pady=10)
    addressEntry.insert(0, data[4])

    genderLabel = Label(update_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=10, sticky='w')
    genderEntry = Entry(update_window, font=('roman', 15, 'bold'))
    genderEntry.grid(row=5, column=1, padx=20, pady=10)
    genderEntry.insert(0, data[5])

    dobLabel = Label(update_window, text='D.O.B.', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=10, sticky='w')
    dobEntry = Entry(update_window, font=('roman', 15, 'bold'))
    dobEntry.grid(row=6, column=1, padx=20, pady=10)
    dobEntry.insert(0, data[6])

    submitButton = ttk.Button(update_window, text='Update', command=update_data)
    submitButton.grid(row=7, columnspan=2, pady=20)


def show_student():
    query = 'SELECT * FROM student'
    mycursor.execute(query)
    rows = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for row in rows:
        studentTable.insert('', END, values=row)



def export_student():
    path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Files', '*.xlsx')])
    if not path:
        return
    student_list = []
    for row in studentTable.get_children():
        student_list.append(studentTable.item(row)['values'])

    if student_list:
        # 9 columns (matching your Treeview)
        df = pd.DataFrame(student_list, columns=['ID', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Time'])  
        try:
            df.to_excel(path, index=False, engine='openpyxl')
            winsound.Beep(1000, 1000)  # 🎶 Play a short beep (frequency=1000Hz, duration=2000ms)
            messagebox.showinfo('Success', f'Data exported successfully!\nFile saved at:\n{path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export data:\n{str(e)}')
    else:
        messagebox.showwarning('Warning', 'No data available to export.')


def connect_database():
    def connect():
        try:
            global con, mycursor
            con = pymysql.connect(host='localhost', user='root', password='Bhuvan@2005')
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Database Connection is successful', parent=connectwindow)
            # Enable all buttons after successful connection
            
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectwindow)
            return
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)    
            query = 'CREATE TABLE IF NOT EXISTS student(id INT NOT NULL PRIMARY KEY,name VARCHAR(30),mobile VARCHAR(10),email VARCHAR(30),address VARCHAR(100),gender VARCHAR(10),dob VARCHAR(20),addedtime VARCHAR(50),time varchar(50))'
            mycursor.execute(query)
        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
            connectwindow.destroy()
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)




    connectwindow = Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry('470x250+730+250')
    connectwindow.title('Database Connection')
    connectwindow.resizable(False, False)

    hostnameLabel = Label(connectwindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectwindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=30, pady=20)

    UsernameLabel = Label(connectwindow, text='User Name', font=('arial', 20, 'bold'))
    UsernameLabel.grid(row=1, column=0, padx=20)
    UsernameEntry = Entry(connectwindow, font=('roman', 15, 'bold'), bd=2)
    UsernameEntry.grid(row=1, column=1, padx=30, pady=20)

    PasswordnameLabel = Label(connectwindow, text='Password', font=('arial', 20, 'bold'))
    PasswordnameLabel.grid(row=2, column=0, padx=20)
    PasswordEntry = Entry(connectwindow, font=('roman', 15, 'bold'), bd=2, show='*')
    PasswordEntry.grid(row=2, column=1, padx=30, pady=20)

    connectButton = ttk.Button(connectwindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, column=0, columnspan=2, pady=20)

# --- Variables for Slider ---
count = 0
text = ''
s = 'BANK Management System'

# --- Slider Text Function ---
def slider():
    global text, count
    if count >= len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(200, slider)

# --- Clock Function ---
def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date} \nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# --- Main Window ---
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1175x680+50+20')
root.resizable(0, 0)
root.title('Bank Management System')

# --- Clock Label ---
datetimeLabel = Label(root, text='', font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=10, y=10)
clock()

# --- Slider Label ---
sliderLabel = Label(root, text='', font=('arial', 28, 'italic bold'), fg='red', width=30)
sliderLabel.place(x=200, y=0)
slider()

# --- Connect Button ---
connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

# --- Left Frame ---
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

button_style = {'font': ('arial', 12, 'bold'), 'bg': '#00BFFF', 'fg': 'white', 'activebackground': '#1E90FF', 'cursor': 'hand2', 'bd': 0}

addstudentButton = Button(leftFrame, text='Add employee', width=25, **button_style, state=DISABLED,command=add_student)
addstudentButton.grid(row=0, column=0, pady=20)

searchstudentButton = Button(leftFrame, text='Search employee', width=25, **button_style, state=DISABLED,command=search_student)
searchstudentButton.grid(row=1, column=0, pady=20)

updatestudentButton = Button(leftFrame, text='Update employee', width=25, **button_style, state=DISABLED,command=update_student)
updatestudentButton.grid(row=2, column=0, pady=20)

showstudentButton = Button(leftFrame, text='Show employee', width=25, **button_style, state=DISABLED,command=show_student)
showstudentButton.grid(row=3, column=0, pady=20)

exportstudentButton = Button(leftFrame, text='Export employee', width=25, **button_style, state=DISABLED,command=export_student)
exportstudentButton.grid(row=4, column=0, pady=20)

deletestudentButton = Button(leftFrame, text='delete employee', width=25, **button_style, state=DISABLED,command=delete_student)
deletestudentButton.grid(row=5, column=0, pady=20)

exitstudentButton = Button(leftFrame, text='Exit', width=25, **button_style, command=iexit)
exitstudentButton.grid(row=6, column=0, pady=20)

# --- Right Frame ---
rightFrame = Frame(root, bg='skyblue')
rightFrame.place(x=350, y=80, width=820, height=600)

# --- Treeview & Scrollbars ---
studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Time'), show='headings')

Scrollbarx = Scrollbar(rightFrame, orient=HORIZONTAL, command=studentTable.xview)
Scrollbary = Scrollbar(rightFrame, orient=VERTICAL, command=studentTable.yview)
studentTable.configure(xscrollcommand=Scrollbarx.set, yscrollcommand=Scrollbary.set)

Scrollbarx.pack(side=BOTTOM, fill=X)
Scrollbary.pack(side=RIGHT, fill=Y)
studentTable.pack(fill=BOTH, expand=1)

# --- Treeview Headings ---
studentTable.heading('Id', text='ID')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('DOB', text='DOB')
studentTable.heading('Added Time', text='Added Time')


# --- Column Widths and Center Alignment ---
studentTable.column('Id', width=75, anchor=CENTER)
studentTable.column('Name', width=250, anchor=CENTER)
studentTable.column('Mobile', width=150, anchor=CENTER)
studentTable.column('Email', width=250, anchor=CENTER)
studentTable.column('Address', width=250, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('DOB', width=250, anchor=CENTER)
studentTable.column('Added Time', width=250, anchor=CENTER)
style=ttk.Style()
style.configure('Treeview',rowwheight=40,font=('arial',10,'bold'),foreground='white',background='black',fieldbackground='black')


root.mainloop()
