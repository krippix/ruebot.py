import logging
import ruebDB

msg_notregistered = ""

def userregister(author_id, author_displayname):
    
    #Prüfen ob Benutzer bereits existiert
    if userexists(author_id):
        logging.info("Benutzer existiert bereits.")
        return "Benutzer existiert bereits."
    
    #User wird in datenbank geschrieben             
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        ruebDB.dbcommit("INSERT INTO users (displayname, id) VALUES (%s, %s)", (author_displayname, author_id))
        return'Benutzer '+author_displayname+' erfolgreich erstellt!'


#--------------------------------------------------------------------------------
#Check stuff
#--------------------------------------------------------------------------------

def userexists(author_id):
    dbanswer = ruebDB.dbrequest('SELECT id FROM users WHERE id=%s', [author_id])
    
    #Check if db-entry of user exists
    if dbanswer is None:
        return False
    
    return True
