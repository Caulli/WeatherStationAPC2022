import datetime

import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
import numpy as np

from database import mydbConnection


# timeframe is hour/day/month

def getValues(msg, timeframe):
    if timeframe == "day":
        the_result = getDay(msg)

    return the_result


def getDay(msg):
    mydb = mydbConnection()
    mycursor = mydb.cursor()
    date_now = datetime.datetime.now()
    date_month_ago = date_now + dateutil.relativedelta.relativedelta(days=-1)
    if msg == "temp" or msg == "light" or msg == "pressure":
        sql = "select {} from py_saxion where time > '{}' ".format(msg, date_month_ago)
        mycursor.execute(sql)
        fetchall = mycursor.fetchall()
        result = []
        for index, x in enumerate(fetchall):
            not_sliced = str(x)
            sliced = not_sliced.replace("(", "").replace(")", "").replace(",", "").replace("'", "")
            result.append(sliced)
        return result
    mydb.close()
    mycursor.close()

