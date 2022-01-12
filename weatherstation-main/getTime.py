import datetime
import dateutil
from database import mydbConnection

def getTime():
    mydb = mydbConnection()
    mycursor = mydb.cursor()
    date_now = datetime.datetime.now()
    date_month_ago = date_now + dateutil.relativedelta.relativedelta(days=-1)
    sql2 = "select time from py_saxion where time > '{}' ".format(date_month_ago)
    mycursor.execute(sql2)
    fetchall = mycursor.fetchall()
    result = []
    for index, x in enumerate(fetchall):
        not_sliced = str(x)
        sliced = not_sliced[2:21]
        result.append(sliced)
    mydb.close()
    mycursor.close()
    return result