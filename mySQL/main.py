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

logInFormAccount.execute("CREATE Database IF NOT EXISTS account")
logInFormAccount.execute("SHOW DATABASES")

for database in logInFormAccount.cursor:
    print(database)

logInFormAccount.execute