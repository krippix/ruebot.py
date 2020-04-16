#python native
import logging
#from datetime import datetime, timedelta
import datetime
import time
#part of project
from ruebot import ruebDB
from ruebot import msg



def updateDisplaynames(author_displayname, author_id):
    try:
        database_displayname = ruebDB.dbrequest("SELECT displayname FROM users where id_pkey=%s", [author_id])
    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    
    
    
    if database_displayname[0] == author_displayname:
        logging.info("username remains unchanged")
        return
    else:
        try:
            ruebDB.dbcommit("UPDATE users SET displayname=%s WHERE id_pkey=%s", (author_displayname, author_id))
            logging.info("username changed from "+str(database_displayname[0])+" to "+str(author_displayname))
        except ruebDB.ruebDatabaseError as e:
            logging.warning("Error username update: "+e)

    #"UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s"


def userexists(author_id):
    
    try:
        dbanswer = ruebDB.dbrequest('SELECT id_pkey FROM users WHERE id_pkey=%s', [author_id])
    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    
    #Check if db-entry of user exists
    if dbanswer is None:
        logging.info("userexists: No")
        return False
    
    return True
#END USEREXISTS



def getToday():
    logging.debug("getting current day: "+str(time.strftime('%Y-%m-%d')))
    return time.strftime('%Y-%m-%d')


def lastSunday():
    #FORMAT: '2020-01-01'
    
    dt = datetime.date.today()
    datum_sonntag = dt - datetime.timedelta(days=dt.isoweekday())
    #end = datum_sonntag + datetime.timedelta(days=6)
    #print(str(end)[0:10]) #Montag
    
    return datum_sonntag

