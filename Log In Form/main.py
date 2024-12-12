# SQL
from mysql import connector
# GUI
from tkinter import *
from tkinter import messagebox

usernameGlobal = ""

# SQL Function for initializing the MySQL Database and its Cursor
def loadDatabase():
    global database, cursor
    # Connect to MySQL Database
    database = connector.connect(
        host = "localhost",
        user = "LogInForm",
        passwd = "8NtJ.Js)AIA1Q@IL",
    )
    # Assign MySQL Cursor to a variable
    cursor = database.cursor()
    # Create necessary databases and table if doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS account")
    cursor.execute("USE account")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (name VARCHAR(255), password VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS pending (name VARCHAR(255), password VARCHAR(255))")

# SQL Function for validating the user info from MySQL Database
def checkAccount(username, password):
    # Check if one or both the entries are empty
    if username.strip() == "Username" and password.strip() == "Password":
        return "Both Username and Password is empty."
    elif username.strip() == "Username":
        return "Username is empty."
    elif password.strip() == "Password":
        return "Password is empty."

    # Filter and Retrieve accounts from database
    filterAccounts = "SELECT * FROM user WHERE name = %s OR password = %s"
    cursor.execute(filterAccounts, (username, password,))

    # Iterate thru results
    status = False
    result = cursor.fetchall()
    resultUsername = None
    resultPassword = None
    for account in result:
        status = True
        resultUsername = account[0]
        resultPassword = account[1]
    
    # Validate found result
    if status == True:
        if username == resultUsername and password == resultPassword:
            global usernameGlobal
            usernameGlobal = username
            return "Login Successful!"
        elif username != resultUsername and password == resultPassword:
            return "Username is incorrect!"
        elif username == resultUsername and password != resultPassword:
            return "Password is incorrect!"
        else:
            return "Both Username and Password are incorrect!"
    else:
        return "Account does not exist!"

# SQL Function for searhing the user password from MySQL Database
def checkAccountName(username):
    # Check if one or both the entries are empty
    if username.strip() == "Username":
        return "Username is empty."

    # Filter and Retrieve accounts from database
    filterAccounts = "SELECT * FROM user WHERE name = %s"
    cursor.execute(filterAccounts, (username,))

    # Iterate thru results
    status = False
    result = cursor.fetchall()
    resultAccount = None
    for account in result:
        status = True
        resultAccount = account
    
    # Validate found result
    if status == True:
        return resultAccount[1] # Return password
    else:
        return None

# SQL Function for storing pending account creations
def pendAccount(username, password):
    # Check if one or both the entries are empty
    if username.strip() == "Username" and password.strip() == "Password":
        messagebox.showinfo("Sign Up Error", "Both Username and Password is empty.")
        return
    elif username.strip() == "Username":
        messagebox.showinfo("Sign Up Error", "Username is empty.")
        return
    elif password.strip() == "Password":
        messagebox.showinfo("Sign Up Error", "Password is empty.")
        return

    storePendingAccount = "INSERT INTO pending (name, password) VALUES (%s, %s)"
    cursor.execute(storePendingAccount, (username, password,))
    database.commit()
    messagebox.showinfo("Account Creation Pending", "To complete account creation, please contact the administrator for approval.")

# SQL Function for getting all of pending account creations
def getPendingAccounts():
    cursor.execute("Select * FROM pending")
    return cursor.fetchall()

# For UI of pending accounts
pendingAccountRows = []

# A function for rendering pending accounts as list
def indexAccountRow():
    global pendingAccountRows

    for index, entry in enumerate(pendingAccountRows):
        entry.free()

    pendingAccountRows.clear()

    for index, entry in enumerate(getPendingAccounts()):
        pendingAccountRows.append(pendingAccountRow(entry[0], entry[1], index))

    window.update()

# A SQL Function for approving pending account creations on MySQL database
def approveAccount(username, password, index):
    removePendingAccount = "DELETE FROM pending WHERE name = %s AND password = %s"
    storeApprovedAccount = "INSERT INTO user (name, password) VALUES (%s, %s)"
    cursor.execute(removePendingAccount, (username, password,))
    cursor.execute(storeApprovedAccount, (username, password,))
    database.commit()

    messagebox.showinfo("Account Approved!", "The account has been approved!")

    global pendingAccountRows
    pendingAccountRows[index].free()
    indexAccountRow()

# A SQL Function for rejecting pending account creations on MySQL database
def disapproveAccount(username, password, index):
    removePendingAccount = "DELETE FROM pending WHERE name = %s AND password = %s"
    cursor.execute(removePendingAccount, (username, password,))
    database.commit()

    messagebox.showinfo("Account Rejected!", "The account has been rejected!")

    global pendingAccountRows
    pendingAccountRows[index].free()
    indexAccountRow()

# A class for UI of pending accounts
class pendingAccountRow:
    def __init__(self, username, password, index):
        self.username = username
        self.password = password
        self.index = index

        self.approveButton = Button(adminPanelWindow)
        self.approveButton.config(text="Approve")
        self.approveButton.bind("<Button>", lambda event: approveAccount(username, password, index))
        self.approveButton.place(x=8, y=96+32*index)

        self.disapproveButton = Button(adminPanelWindow)
        self.disapproveButton.config(text="Reject")
        self.disapproveButton.bind("<Button>", lambda event: disapproveAccount(username, password, index))
        self.disapproveButton.place(x=72, y=96+32*index)

        self.nameLabel = Label(adminPanelWindow)
        self.nameLabel.config(text=username)
        self.nameLabel.place(x=128, y=96+32*index)

        self.passwordLabel =  Label(adminPanelWindow)
        self.passwordLabel.config(text=password)
        self.passwordLabel.place(x=304, y=96+32*index)

    # A function for freeing the UIs after using it
    def free(self):
        self.approveButton.destroy()
        self.disapproveButton.destroy()
        self.nameLabel.destroy()
        self.passwordLabel.destroy()

# A function for closing admin panel
def closeAppWindow(event):
    global adminPanelWindow
    adminPanelWindow.destroy()

# A function for displaying admin panel
def loadAdminPanel():
    global adminPanelWindow
    adminPanelWindow = Toplevel()
    adminPanelWindow.title("Admin Panel")
    adminPanelWindow.geometry("480x480")

    labelTitle = Label(adminPanelWindow)
    labelTitle.config(text="Admin Panel - Account Management", font=("Arial", 20), fg="#888583", bg="#ECECEC") 
    labelTitle.place(x=0, y=0)
    adminPanelWindow.update()
    labelTitle.place(x=(240-labelTitle.winfo_width()/2), y=8)

    labelDesc = Label(adminPanelWindow)
    labelDesc.config(text="Pending Accounts for Approval", font=("Arial", 10), fg="#888583")
    labelDesc.place(x=0, y=0)
    adminPanelWindow.update()
    labelDesc.place(x=(256-labelDesc.winfo_width()/2), y=48)

    labelAction = Label(adminPanelWindow)
    labelAction.config(text="Action:", font=("Arial", 10))
    labelAction.place(x=0, y=0)
    adminPanelWindow.update()
    labelAction.place(x=8, y=72)

    labelUsername = Label(adminPanelWindow)
    labelUsername.config(text="Username:", font=("Arial", 10))
    labelUsername.place(x=0, y=0)
    adminPanelWindow.update()
    labelUsername.place(x=128, y=72)

    labelPassword = Label(adminPanelWindow)
    labelPassword.config(text="Password:", font=("Arial", 10))
    labelPassword.place(x=0, y=0)
    adminPanelWindow.update()
    labelPassword.place(x=304, y=72)

    indexAccountRow()
    adminPanelWindow.mainloop()

# A function for closing app window
def closeAppWindow(event):
    global appWindow
    appWindow.destroy()

# A function for displaying Main App Window
def loadAppWindow():
    global appWindow
    appWindow = Toplevel()
    appWindow.title("App")
    appWindow.geometry("480x480")

    labelHomeTitle = Label(appWindow)
    labelHomeTitle.config(text="Hello " + usernameGlobal + "! Welcome back!", font=("Arial", 20), fg="#888583")
    labelHomeTitle.place(x=0, y=0)
    appWindow.update()
    labelHomeTitle.place(x=(256-labelHomeTitle.winfo_width()/2), y=32)

    buttonLogOut = Button(appWindow)
    buttonLogOut.config (width=28, borderwidth=4, relief=FLAT, font=("Arial", 16), text="Log Out", fg="#FFFFFF", bg="#70C5C0")
    buttonLogOut.bind("<Button>", closeAppWindow)
    buttonLogOut.place(x=0, y=0)
    appWindow.update()
    buttonLogOut.place(x=(256-buttonLogOut.winfo_width()/2), y=360)

    appWindow.mainloop()

noOfIncorrects = 0 # A variable to track incorrect attempts

# A function to warn user when invalid entries occured
def signInFailed(message, showIncorrects):
    if showIncorrects:
        messagebox.showerror("Sign In Failed", (message + "\n\n You have " + str(3-noOfIncorrects)) + " attempts to sign in.")
    else:
        messagebox.showerror("Sign In Failed", message)

# A TKinter event function used when a user presses the Sign In button
def signIn(event):
    global noOfIncorrects

    username = entryUsername.get()
    password = entryPassword.get()

    if noOfIncorrects < 3:
        if username == "admin" and password == "admin":
            loadAdminPanel()
        else:
            status = checkAccount(username, password)

            if status == "Login Successful!":
                loadAppWindow()
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

# A TKinter Event for Username Recovery Entry
def entryUsernameRecoveryEvent(event):
    global entryUsernameRecovery

    event = str(event)
    if event == "<FocusIn event>":
        if entryUsernameRecovery.get() == "Username":
            entryUsernameRecovery.delete(0, "end")
            entryUsernameRecovery.config(fg="#000000")
    elif event == "<FocusOut event>":
        if entryUsernameRecovery.get().strip() == "":
            entryUsernameRecovery.insert(0, "Username")
            entryUsernameRecovery.config(fg="#888583")

# A TKinter event function for validating username in password recovery
def validateUsername(event):
    status = checkAccountName(entryUsernameRecovery.get())

    if status != None:
        messagebox.showinfo("Account Recovery: Account Found!", "Account Exists, the password is: " + status)
    else:
        messagebox.showerror("Account Recovery: Account Not Found!", "Account does not Exist!")

# A TKinter event function used when a user presses the Forgot Password button
def loadPasswordRecovery(event):
    recoveryWindow = Toplevel()
    recoveryWindow.title("App")
    recoveryWindow.geometry("480x480")

    labelTitle = Label(recoveryWindow)
    labelTitle.config(text="Forgot Password?", font=("Arial", 20), fg="#888583")
    labelTitle.place(x=0, y=0)
    recoveryWindow.update()
    labelTitle.place(x=(256-labelTitle.winfo_width()/2), y=32)

    labelDesc = Label(recoveryWindow)
    labelDesc.config(text="Type your username below to recover password", font=("Arial", 12), fg="#888583")
    labelDesc.place(x=0, y=0)
    recoveryWindow.update()
    labelDesc.place(x=(256-labelDesc.winfo_width()/2), y=184)

    global entryUsernameRecovery
    entryUsernameRecovery = Entry(recoveryWindow)
    entryUsernameRecovery.insert(0, "Username")
    entryUsernameRecovery.bind("<FocusIn>", entryUsernameRecoveryEvent)
    entryUsernameRecovery.bind("<FocusOut>", entryUsernameRecoveryEvent)
    entryUsernameRecovery.config(width=28, borderwidth=8, relief=FLAT, font=("Arial", 16), fg="#888583")
    entryUsernameRecovery.place(x=0, y=0)
    recoveryWindow.update()
    entryUsernameRecovery.place(x=(256-entryUsername.winfo_width()/2), y=232)

    buttonSearch = Button(recoveryWindow)
    buttonSearch.config (width=28, borderwidth=4, relief=FLAT, font=("Arial", 16), text="Search", fg="#FFFFFF", bg="#70C5C0")
    buttonSearch.bind("<Button>", validateUsername)
    buttonSearch.place(x=0, y=0)
    window.update()
    buttonSearch.place(x=(256-buttonSearch.winfo_width()/2), y=360)

    recoveryWindow.mainloop()

# A TKinter Event for Username Entry
def entrySignUpUsernameEvent(event):
    global entrySignUpUsername

    event = str(event)
    if event == "<FocusIn event>":
        if entrySignUpUsername.get() == "Username":
            entrySignUpUsername.delete(0, "end")
            entrySignUpUsername.config(fg="#000000")
    elif event == "<FocusOut event>":
        if entrySignUpUsername.get().strip() == "":
            entrySignUpUsername.insert(0, "Username")
            entrySignUpUsername.config(fg="#888583")

# A TKinter Event function for Password Entry
def entrySignUpPasswordEvent(event):
    global entrySignUpPassword

    event = str(event)
    if event == "<FocusIn event>":
        if entrySignUpPassword.get() == "Password":
            entrySignUpPassword.delete(0, "end")
            entrySignUpPassword.config(show="*")
            entrySignUpPassword.config(fg="#000000")
    elif event == "<FocusOut event>":
        if entrySignUpPassword.get().strip() == "":
            entrySignUpPassword.insert(0, "Password")
            entrySignUpPassword.config(show="")
            entrySignUpPassword.config(fg="#888583")
        else:
            entrySignUpPassword.config(show="*")
            entrySignUpPassword.config(fg="#000000")

# A TKinter Event function for Sign Up Button
def buttonSignUpEvent(event):
    pendAccount(entrySignUpUsername.get(), entrySignUpPassword.get())

# A TKinter event function used when a user presses the Sign In button
def loadSignUpWindow(event):
    global signUpWindow
    signUpWindow = Toplevel()
    signUpWindow.title("Sign Up Form")
    signUpWindow.geometry("512x576")
    signUpWindow.config(background="#C86F70")

    frameBG = Frame(signUpWindow)
    frameBG.config(background="#ECECEC", width=448, height=428)
    frameBG.place(x=32, y=48)

    global imageProfile
    labelProfile = Label(signUpWindow)
    labelProfile.config(image=imageProfile, bg="white")
    labelProfile.place(x=197, y=18)

    labelTitle = Label(signUpWindow)
    labelTitle.config(text="Member Sign Up", font=("Arial", 20), fg="#888583", bg="#ECECEC") 
    labelTitle.place(x=0, y=0)
    signUpWindow.update()
    labelTitle.place(x=(256-labelTitle.winfo_width()/2), y=168)

    global entrySignUpUsername
    entrySignUpUsername = Entry(signUpWindow)
    entrySignUpUsername.insert(0, "Username")
    entrySignUpUsername.bind("<FocusIn>", entrySignUpUsernameEvent)
    entrySignUpUsername.bind("<FocusOut>", entrySignUpUsernameEvent)
    entrySignUpUsername.config(width=28, borderwidth=8, relief=FLAT, font=("Arial", 16), fg="#888583")
    entrySignUpUsername.place(x=0, y=0)
    signUpWindow.update()
    entrySignUpUsername.place(x=(256-entrySignUpUsername.winfo_width()/2), y=232)

    global entrySignUpPassword
    entrySignUpPassword = Entry(signUpWindow)
    entrySignUpPassword.insert(0, "Password")
    entrySignUpPassword.bind("<FocusIn>", entrySignUpPasswordEvent)
    entrySignUpPassword.bind("<FocusOut>", entrySignUpPasswordEvent)
    entrySignUpPassword.config(width=28, borderwidth=8, relief=FLAT, font=("Arial", 16), fg="#888583")
    entrySignUpPassword.place(x=0, y=0)
    signUpWindow.update()
    entrySignUpPassword.place(x=(256-entrySignUpPassword.winfo_width()/2), y=296)

    buttonSignUp = Button(signUpWindow)
    buttonSignUp.config (width=28, borderwidth=4, relief=FLAT, font=("Arial", 16), text="Sign Up", fg="#FFFFFF", bg="#70C5C0")
    buttonSignUp.bind("<Button>", buttonSignUpEvent)
    buttonSignUp.place(x=0, y=0)
    signUpWindow.update()
    buttonSignUp.place(x=(256-buttonSignUp.winfo_width()/2), y=360)

    signUpWindow.mainloop()

# A TKinter Event for Username Entry
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

# A TKinter Event function for Password Entry
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

# A function for loading Log In Form UI Elements
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
    buttonForgotPassword.bind("<Button>", loadPasswordRecovery)
    buttonForgotPassword.place(x=0, y=0)
    window.update()
    buttonForgotPassword.place(x=432-buttonForgotPassword.winfo_width(), y=432)

    labelSignUp = Label(window)
    labelSignUp.config(borderwidth=4 ,font=("Arial", 10), text="Don't have an account?", fg="#FFFFFF", bg="#C86F70")
    labelSignUp.place(x=0, y=0)

    buttonSignUp = Button(window)
    buttonSignUp.config(relief=FLAT, font=("Arial", 10, "underline"), text="Sign Up", fg="#FFFFFF", bg="#C86F70")
    buttonSignUp.bind("<Button>", loadSignUpWindow)
    buttonSignUp.place(x=0, y=0)

    window.update()
    labelSignUp.place(x=(256-(labelSignUp.winfo_width()+buttonSignUp.winfo_width())/2), y=528)
    buttonSignUp.place(x=(256-(labelSignUp.winfo_width()+buttonSignUp.winfo_width())/2+labelSignUp.winfo_width()), y=524)

# A function for loading all necessary things
def load():
    loadDatabase()
    loadWindow()

# A function for main function
def main():
    load()

    global window
    window.mainloop()

if __name__ == "__main__":
    main()