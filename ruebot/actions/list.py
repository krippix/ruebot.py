#python native
import logging
import time
#part of project
from ruebot.actions import ruebDB
from ruebot import msg
#external
from texttable import Texttable




#LIST PRICE START
def prices(author_id):
    #List all prices of the current day and daytime
        
    #checks if it works
    if time.strftime("%p"):                
        
        #AM = 0
        if time.strftime("%p") ==  "AM":
            daytime = False
        elif time.strftime("%p") ==  "PM":
            daytime = True
                
    else:
        logging.error("Couldn't retrieve time!")
        return "Fehler - Eintrag konnte nicht erstellt werden, bitte versuche es später erneut."           
                
    #       
    
    try:
        #Retrieve whether user is marked as pirate
        answer_tuple = ruebDB.dbrequest("SELECT pirate FROM users WHERE id_pkey=%s", [author_id],)
        logging.info(answer_tuple)
        
        #Check if pirate is true
        if answer_tuple[0] == 'true':
            logging.debug("PIRATE = TRUE")
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id_pkey WHERE t.date=NOW()::date AND daytime=%s AND pirate='true' ORDER BY t.price DESC",(daytime,))]
            tablename = ":pirate_flag:Piratendaten:pirate_flag:: "
            
            if len(answer_tuple) == 0:
                logging.info("Keine Rübenpreise verfügbar")
                return "Bisher sind keine :pirate_flag:-Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."
        
        
        #Regular users:
        else:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id_pkey WHERE t.date=NOW()::date AND daytime=%s AND NOT pirate='true' ORDER BY t.price DESC",(daytime,))]
            tablename = "Nomale Daten: "
            if len(answer_tuple) == 0:
                logging.info("Keine Rübenpreise verfügbar")
                return "Bisher sind keine Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."

    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    #except TypeError:

    
    
    #prints input into string
    t = Texttable()
    t.add_row(["Benutzer","Preis"])
    
    for x in answer_tuple:
        t.add_row(x)
    
    answer = t.draw()
    
    print(answer)
    
    return tablename+"\n```\n"+answer+"```"
#END LIST PRICE



#LIST USERS | LIST USER <USERNAME> START
def users(user_input):
    #pass None if all users should be displayed
    if user_input is None:
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE NOT (u.id_pkey = 0 )",(),)]
        except ruebDB.ruebDatabaseError:
            logging.error("LIST - USERS: "+ruebDB.ruebDatabaseError)
            return msg.DbError()
        
    
        if len(answer_tuple) == 0:
            logging.error("Fehler - Keine Benutzer gefunden.")
            return "Fehler - Keine Benutzer gefunden."
    #Username is defined
    else:

        user_input = user_input.lower()
        
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE LOWER(u.displayname) LIKE %s LIMIT 10",[user_input+"%"],)]
        except ruebDB.ruebDatabaseError:
            logging.error("LIST - USERS: "+ruebDB.ruebDatabaseError)
            return msg.DbError()
        
    
        if len(answer_tuple) == 0:
            logging.error("Fehler - Keine Benutzer gefunden.")
            return "Fehler - Keine Benutzer gefunden."
    
    
    
    #prints input into string
    t = Texttable()
    t.add_row(["Benutzer","Frucht", "Freundescode", "pirat / banned"])
    

    for x in answer_tuple:
        t.add_row(x)
    
    answer = t.draw()
    
    return "```\n"+answer+"```"         
#LIST USERS | LIST USER <USERNAME> END    



#LIST PRICEHISTORY <USER>
def pricehistory():
    #Lists pricehistory since last monday
    print()
    
    
    
    
    
    
    
    
    
    
#LIST PRICEHISTORY <USER END
