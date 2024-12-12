import tkinter as tk
from tkinter import messagebox

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

def displayApp():
    global uname

    appWindow = tk.Toplevel()
    appWindow.title("App")
    appWindow.geometry("480x480")

    labelHomeTitle = tk.Label(appWindow)
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
    global uanme, pword, noOfIncorrects, entryUsername, entryPassword

    username = entryUsername.get()
    password = entryPassword.get()

    if noOfIncorrects < 3:
        if username == uname and password == pword:
            displayApp()
        else:
            if username == "Username" and password == "Password":
                signInFailed("Username and Password has left blank.", False)
            elif username != uname and password == pword:
                signInFailed("Username is incorrect", True)
                noOfIncorrects += 1
            elif username == uname and password != pword:
                signInFailed("Password is incorrect", True)
                noOfIncorrects += 1
            else:
                signInFailed("Username and Password is both incorrect", True)
                noOfIncorrects += 1
    else:
        messagebox.showerror("Unable to Sign In", "You have reached the maximum Sign In attempts")

def forgotPassword(event):
    global pword
    messagebox.showinfo("Password Recovery", "The password is " + pword)

def signUp(event):
    messagebox.showinfo("Sign Up Request", "You may need to contact the administrator in order to create an account.")

def load():
    global window
    window = tk.Tk()
    window.title("Log In Form")
    window.geometry("512x576")
    window.config(background="#C86F70")

    frameBG = tk.Frame(window)
    frameBG.config(background="#ECECEC", width=448, height=428)
    frameBG.place(x=(512-448)/2, y=(576-448)/2+16)

    global imageProfile
    imageProfile = tk.PhotoImage(file="profile.png").subsample(2,2)

    labelProfile = tk.Label(window)
    labelProfile.config(image=imageProfile, bg="white")
    labelProfile.place(x=(512-236/2)/2, y=(576-448-236/2+8)/2)

    global labelTitle
    labelTitle = tk.Label(window)
    labelTitle.config(text="Member Login", font=("Arial", 20), fg="#888583", bg="#ECECEC") 
    labelTitle.place(x=0, y=0)
    window.update()
    labelTitle.place(x=(512-labelTitle.winfo_width())/2, y=128+32+8)

    global entryUsername
    entryUsername = tk.Entry(window)
    entryUsername.insert(0, "Username")
    entryUsername.bind("<FocusIn>", entryUsernameEvent)
    entryUsername.bind("<FocusOut>", entryUsernameEvent)
    entryUsername.config(width=28, borderwidth=8, relief=tk.FLAT, font=("Arial", 16), fg="#888583")
    entryUsername.place(x=0, y=0)
    window.update()
    entryUsername.place(x=(512-entryUsername.winfo_width())/2, y=128+64+32+8)

    global entryPassword
    entryPassword = tk.Entry(window)
    entryPassword.insert(0, "Password")
    entryPassword.bind("<FocusIn>", entryPasswordEvent)
    entryPassword.bind("<FocusOut>", entryPasswordEvent)
    entryPassword.config(width=28, borderwidth=8, relief=tk.FLAT, font=("Arial", 16), fg="#888583")
    entryPassword.place(x=0, y=0)
    window.update()
    entryPassword.place(x=(512-entryPassword.winfo_width())/2, y=256+32+8)

    global buttonSignIn
    buttonSignIn = tk.Button(window)
    buttonSignIn.config (width=28, borderwidth=4, relief=tk.FLAT, font=("Arial", 16), text="Sign In", fg="#FFFFFF", bg="#70C5C0")
    buttonSignIn.bind("<Button>", signIn)
    buttonSignIn.place(x=0, y=0)
    window.update()
    buttonSignIn.place(x=(512-buttonSignIn.winfo_width())/2, y=256+64+32+8)

    global checkButtonRemember
    checkButtonRemember = tk.Checkbutton(window)
    checkButtonRemember.config(font=("Arial", 11), text="Remember Me", relief=tk.FLAT, fg="#888583", bg="#ECECEC")
    checkButtonRemember.place(x=64+8+4, y=256+128+32+16)

    global buttonForgotPassword
    buttonForgotPassword = tk.Button(window)
    buttonForgotPassword.config(font=("Arial", 11, "underline"), text="Forgot Password?", relief=tk.FLAT, fg="#888583", bg="#ECECEC")
    buttonForgotPassword.bind("<Button>", forgotPassword)
    buttonForgotPassword.place(x=0, y=0)
    window.update()
    buttonForgotPassword.place(x=512-64-16-buttonForgotPassword.winfo_width(), y=256+128+32+16)

    global labelSignUp
    labelSignUp = tk.Label(window)
    labelSignUp.config(borderwidth=4 ,font=("Arial", 10), text="Don't have an account?", fg="#FFFFFF", bg="#C86F70")
    labelSignUp.place(x=0, y=0)

    global buttonSignUp
    buttonSignUp = tk.Button(window)
    buttonSignUp.config(relief=tk.FLAT, font=("Arial", 10, "underline"), text="Sign Up", fg="#FFFFFF", bg="#C86F70")
    buttonSignUp.bind("<Button>", signUp)
    buttonSignUp.place(x=0, y=0)

    window.update()
    labelSignUp.place(x=(512-labelSignUp.winfo_width()-buttonSignUp.winfo_width())/2, y=576-32-16)
    buttonSignUp.place(x=(512-labelSignUp.winfo_width()-buttonSignUp.winfo_width())/2+labelSignUp.winfo_width(), y=576-32-16-4)

def main():
    global window
    load()
    window.mainloop()

if __name__ == "__main__":
    main()