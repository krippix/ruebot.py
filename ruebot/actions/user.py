#python native
import logging
#part of project
from ruebot import ruebDB
from ruebot import getInfo
from ruebot import msg


def delete(author_id):
    if getInfo.userexists(author_id):
        try:
            ruebDB.dbcommit("UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s", [author_id])
            ruebDB.dbcommit("DELETE FROM users WHERE id_pkey=%s", [author_id])
            logging.info("user has been deleted!")
            return "Benutzer wurde erfolgreich gelöscht!"
                
        except ruebDB.ruebDatabaseError as e:
            logging.error("USER DELETE: "+e)
            return msg.DbError()
    else:
        return msg.noUser()   
#END USERDELETE


def register(author_id, author_displayname):

    
    #check if user already exists
    if getInfo.userexists(author_id):
        logging.info("user already exists.")
        return "Fehler - Benutzer existiert bereits."
    
    #write new user into database            
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        try:
            ruebDB.dbcommit("INSERT INTO users (displayname, id_pkey, friendcode, fruits_id_fkey, pirate) VALUES (%s, %s, %s, %s, %s)", (author_displayname, author_id, "<unknown>", 1, "<unknown>"))
            return 'Benutzer '+author_displayname+' erfolgreich erstellt!'
            
        except ruebDB.ruebDatabaseError as e:
            logging.error("USER REGISTER: "+e)
            return msg.DbError()
#END USER REGISTER