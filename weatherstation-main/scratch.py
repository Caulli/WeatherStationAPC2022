import mysql.connector

new_mydb = mysql.connector.connect(
    host="groep8.mysql.database.azure.com",
    user="groep8@groep8",
    password="123qwe,./",
    database="saxionsensors"
)

mydb = mysql.connector.connect(
    host="group8-basic.mysql.database.azure.com",
    user="azuregroup8@group8-basic",
    password="Terragroup!",
    database="saxionsensors"
)

mycursor = new_mydb.cursor()
mycursor.execute("select count(device_id) from new_eui_70b3d5499d2ec797")

# fetch all the matching rows
result = mycursor.fetchall()
print(result)

mycursor1 = mydb.cursor()
mycursor1.execute("select count(device_id) from eui_70b3d5499d2ec797")

# fetch all the matching rows
result = mycursor1.fetchall()
print(result)

# mycursor1 = mydb.cursor()
# mycursor1.execute("select temp, time from lht_gronau where temp > 600")
# # fetch all the matching rows
# result = mycursor1.fetchall()
# print(result)