import mysql.connector

class mySQLAccount:
    def __init__(self, name, password):
        self.database = mysql.connector.connect(
            host="localhost",
            user=name,
            passwd=password
        )

        self.cursor = self.database.cursor()

    def execute(self, code):
        self.cursor.execute(code)

logInFormAccount = mySQLAccount("LogInForm", "8NtJ.Js)AIA1Q@IL")

logInFormAccount.execute("CREATE DATABASE IF NOT EXISTS account")
logInFormAccount.execute("SHOW DATABASES")

for database in logInFormAccount.cursor:
    print(database)

logInFormAccount.execute("USE account")
logInFormAccount.execute("CREATE TABLE IF NOT EXISTS user (name VARCHAR(255), password VARCHAR(255))")

insertAccount = "INSERT INTO user (name, password) VALUES (%s, %s)"
account = ("admin1", "admin2")

logInFormAccount.cursor.execute(insertAccount, account)
logInFormAccount.database.commit()
print(logInFormAccount.cursor.rowcount, "record inserted.")

logInFormAccount.execute("SELECT * FROM user")
result = logInFormAccount.cursor.fetchall()

for s in result:
    print(s)