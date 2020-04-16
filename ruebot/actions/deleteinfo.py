#python native
import logging
#part of project
from ruebot import getInfo
from ruebot import msg
from ruebot import ruebDB
#external




def friendcode(author_id):
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    try:
        ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",("<unknown>",author_id))
        return "Freundescode erfolgreich gelöscht!"
    
    except ruebDB.ruebDatabaseError as e:
        logging.error("DELTE INFO FC: "+e)
        return msg.DbError()       
#DELETE INFO FC END