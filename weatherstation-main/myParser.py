
def myParsing(msg, text):
    valFront = msg.find('"' + str(text) + '":"') + len('"' + str(text) + '":"')
    temp = msg[valFront:]
    finalmsg = temp.partition('"')[0]
    finalmsg = finalmsg.replace("-", "_") # for device_id to support the sql table
    return finalmsg
