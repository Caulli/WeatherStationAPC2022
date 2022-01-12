import mysql.connector
from mysql.connector import Error

def mydbConnection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="groep8.mysql.database.azure.com",
            user="groep8@groep8",
            password="123qwe,./",
            database="saxionsensors"
        )
        # print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return mydb
