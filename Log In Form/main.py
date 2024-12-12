# SQL
from mysql import connector
# GUI
from tkinter import *
from tkinter import messagebox


# SQL Function for initializing the MySQL Database and its cursor
def loadDatabase():
    global database, cursor

    database = connector.connect(
        host = "localhost",
        user = "LogInForm",
        passwd = "8NtJ.Js)AIA1Q@IL",
    )

    cursor = database.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS account")
    cursor.execute("USE account")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (name VARCHAR(255), password VARCHAR(255))")

def checkAccount(username, password):
    if username.strip() == "Username" and password.strip() == "Password":
        return "Both Username and Password is empty."
    elif username.strip() == "Username":
        return "Username is empty."
    elif password.strip() == "Password":
        return "Password is empty."

    filterAccounts = "SELECT * FROM user WHERE name = %s OR password = %s"
    cursor.execute(filterAccounts, (username, password,))

    status = False
    result = cursor.fetchall()
    resultUsername = None
    resultPassword = None
    for account in result:
        status = True
        resultUsername = account[0]
        resultPassword = account[1]
    
    if status == True:
        if username == resultUsername and password == resultPassword:
            return "Login Successful!"
        elif username != resultUsername and password == resultPassword:
            return "Username is incorrect!"
        elif username == resultUsername and password != resultPassword:
            return "Password is incorrect!"
        else:
            return "Both Username and Password are incorrect!"
    else:
        return "Account does not exist!"

'''
    Main window Event Functions
'''

def entryUsernameEvent(event):
    global entryUsername

    event = str(event)
    if event == "<FocusIn event>":
        if entryUsername.get() == "Username":
            entryUsername.delete(0, "end")
            entryUsername.config(fg="#000000")
    elif event == "<FocusOut event>":
        if entryUsername.get().strip() == "":
            entryUsername.insert(0, "Username")
            entryUsername.config(fg="#888583")

def entryPasswordEvent(event):
    global entryPassword

    event = str(event)
    if event == "<FocusIn event>":
        if entryPassword.get() == "Password":
            entryPassword.delete(0, "end")
            entryPassword.config(show="*")
            entryPassword.config(fg="#000000")
    elif event == "<FocusOut event>":
        if entryPassword.get().strip() == "":
            entryPassword.insert(0, "Password")
            entryPassword.config(show="")
            entryPassword.config(fg="#888583")
        else:
            entryPassword.config(show="*")
            entryPassword.config(fg="#000000")

uname = "admin"
pword = "1234567890"

'''
    App window Event Functions
'''

def displayApp():
    global uname

    appWindow = Toplevel()
    appWindow.title("App")
    appWindow.geometry("480x480")

    labelHomeTitle = Label(appWindow)
    labelHomeTitle.config(text="Hello " + uname + "! Welcome back!")
    labelHomeTitle.pack()

    appWindow.mainloop()

def signInFailed(message, showIncorrects):
    if showIncorrects:
        messagebox.showerror("Sign In Failed", (message + "\n\n You have " + str(3-noOfIncorrects)) + " attempts to sign in.")
    else:
        messagebox.showerror("Sign In Failed", message)

noOfIncorrects = 0 # Tracks incorrect attempts
def signIn(event):
    global noOfIncorrects

    if noOfIncorrects < 3:
        status = checkAccount(entryUsername.get(), entryPassword.get())

        if status == "Login Successful!":
            displayApp()
        else:
            if (status == "Both Username and Password is empty." or
                status == "Username is empty." or
                status == "Password is empty."):
                signInFailed(status, False)
            else:
                signInFailed(status, True)
                noOfIncorrects += 1
    else:
        messagebox.showerror("Unable to Sign In", "You have reached the maximum Sign In attempts")

def forgotPassword(event):
    global pword
    messagebox.showinfo("Password Recovery", "The password is " + pword)

def signUp(event):
    messagebox.showinfo("Sign Up Request", "You may need to contact the administrator in order to create an account.")

def loadWindow():
    global window
    window = Tk()
    window.title("Log In Form")
    window.geometry("512x576")
    window.config(background="#C86F70")

    frameBG = Frame(window)
    frameBG.config(background="#ECECEC", width=448, height=428)
    frameBG.place(x=32, y=48)

    global imageProfile
    imageProfile = PhotoImage(file="profile.png").subsample(2,2)

    labelProfile = Label(window)
    labelProfile.config(image=imageProfile, bg="white")
    labelProfile.place(x=197, y=18)

    labelTitle = Label(window)
    labelTitle.config(text="Member Login", font=("Arial", 20), fg="#888583", bg="#ECECEC") 
    labelTitle.place(x=0, y=0)
    window.update()
    labelTitle.place(x=(256-labelTitle.winfo_width()/2), y=168)

    global entryUsername
    entryUsername = Entry(window)
    entryUsername.insert(0, "Username")
    entryUsername.bind("<FocusIn>", entryUsernameEvent)
    entryUsername.bind("<FocusOut>", entryUsernameEvent)
    entryUsername.config(width=28, borderwidth=8, relief=FLAT, font=("Arial", 16), fg="#888583")
    entryUsername.place(x=0, y=0)
    window.update()
    entryUsername.place(x=(256-entryUsername.winfo_width()/2), y=232)

    global entryPassword
    entryPassword = Entry(window)
    entryPassword.insert(0, "Password")
    entryPassword.bind("<FocusIn>", entryPasswordEvent)
    entryPassword.bind("<FocusOut>", entryPasswordEvent)
    entryPassword.config(width=28, borderwidth=8, relief=FLAT, font=("Arial", 16), fg="#888583")
    entryPassword.place(x=0, y=0)
    window.update()
    entryPassword.place(x=(256-entryPassword.winfo_width()/2), y=296)

    buttonSignIn = Button(window)
    buttonSignIn.config (width=28, borderwidth=4, relief=FLAT, font=("Arial", 16), text="Sign In", fg="#FFFFFF", bg="#70C5C0")
    buttonSignIn.bind("<Button>", signIn)
    buttonSignIn.place(x=0, y=0)
    window.update()
    buttonSignIn.place(x=(256-buttonSignIn.winfo_width()/2), y=360)

    checkButtonRemember = Checkbutton(window)
    checkButtonRemember.config(font=("Arial", 11), text="Remember Me", relief=FLAT, fg="#888583", bg="#ECECEC")
    checkButtonRemember.place(x=76, y=432)

    buttonForgotPassword = Button(window)
    buttonForgotPassword.config(font=("Arial", 11, "underline"), text="Forgot Password?", relief=FLAT, fg="#888583", bg="#ECECEC")
    buttonForgotPassword.bind("<Button>", forgotPassword)
    buttonForgotPassword.place(x=0, y=0)
    window.update()
    buttonForgotPassword.place(x=432-buttonForgotPassword.winfo_width(), y=432)

    labelSignUp = Label(window)
    labelSignUp.config(borderwidth=4 ,font=("Arial", 10), text="Don't have an account?", fg="#FFFFFF", bg="#C86F70")
    labelSignUp.place(x=0, y=0)

    buttonSignUp = Button(window)
    buttonSignUp.config(relief=FLAT, font=("Arial", 10, "underline"), text="Sign Up", fg="#FFFFFF", bg="#C86F70")
    buttonSignUp.bind("<Button>", signUp)
    buttonSignUp.place(x=0, y=0)

    window.update()
    labelSignUp.place(x=(256-(labelSignUp.winfo_width()-buttonSignUp.winfo_width())/2), y=528)
    buttonSignUp.place(x=(256-(labelSignUp.winfo_width()-buttonSignUp.winfo_width())/2+labelSignUp.winfo_width()), y=524)

def load():
    loadDatabase()
    loadWindow()

def main():
    load()

    global window
    window.mainloop()

if __name__ == "__main__":
    main()