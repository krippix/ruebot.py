#python native
import logging
#from datetime import datetime, timedelta
import datetime
import time
#part of project
from ruebot.actions import ruebDB
from ruebot import msg



def updateDisplaynames(author_displayname, author_id):
    try:
        database_displayname = ruebDB.dbrequest("SELECT displayname FROM users where id_pkey=%s", [author_id])
    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    
    
    
    if database_displayname[0] == author_displayname:
        logging.info("Username remains unchanged")
        return
    else:
        try:
            ruebDB.dbcommit("UPDATE users SET displayname=%s WHERE id_pkey=%s", (author_displayname, author_id))
        except ruebDB.ruebDatabaseError as msg:
            logging.warning("UPDATE USERNAME: "+msg)

    #"UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s"



def userexists(author_id):
    
    try:
        dbanswer = ruebDB.dbrequest('SELECT id_pkey FROM users WHERE id_pkey=%s', [author_id])
    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    
    #Check if db-entry of user exists
    if dbanswer is None:
        return False
    
    return True
#END USEREXISTS



def getToday():
    return time.strftime('%Y-%m-%d')


def lastSunday():
    #FORMAT: '2020-01-01'
    
    dt = datetime.date.today()
    datum_sonntag = dt - datetime.timedelta(days=dt.isoweekday())
    end = datum_sonntag + datetime.timedelta(days=6)
    print(str(end)[0:10]) #Montag
    
    return datum_sonntag

