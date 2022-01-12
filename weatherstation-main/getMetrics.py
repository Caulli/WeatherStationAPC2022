import datetime

from database import mydbConnection
from myParser import myParsing

def getMetric(msg, time):
    mydb = mydbConnection()
    mycursor = mydb.cursor()
    # if msg != "temp" or msg != "light" or msg != "time" or msg != "pressure":
    #     mycursor.execute("select raw_json from py_saxion where time like '2021_12_03%' ")
    #     result = mycursor.fetchall()
    #     finalmsg = []
    #     for row in result:
    #         finalmsg = myParsing(msg, row)
    #
    #     mycursor.close()
    #     mydb.close
    #     return finalmsg
    # else:
    if  msg == "temp" or msg == "light" or msg == "pressure":
        mycursor.execute("select {} from py_saxion order by id desc limit 1".format(msg))
        fetchall = mycursor.fetchall()
        result = []
        for index, x in enumerate(fetchall):
            not_sliced = str(x)
            sliced = not_sliced.replace("(", "").replace(")", "").replace(",", "").replace("'", "")
            result.append(sliced)
        return result
        mycursor.close()
        mydb.close
