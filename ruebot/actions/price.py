#python native
import logging
import time
#part of project
from ruebot import ruebDB
from ruebot import msg
import ruebot.getInfo
#external



def add(turnip_price, author_id):
    #add price to db entry of user
    
    
    #check if user exists
    if not ruebot.getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    
    #Check if price is viable
    try:
        turnip_price = int(turnip_price)
    except Exception:
        logging.info('"'+str(turnip_price)+'" ist kein Gültiger Preis.')
        return '"'+str(turnip_price)+'" ist kein Gültiger Preis.'
    
    #Check if turnip price is in allowed range
    if turnip_price < 1 or turnip_price > 1000:
        logging.info('Der Preis muss zwischen 1 und 1000 liegen!')
        return 'Der Preis muss zwischen 1 und 1000 liegen!'
    else:
        
        #Check if time can be looked up
        if not time.strftime("%p"):
            logging.error("Couldn't retrieve time!")
            return "Fehler - Eintrag konnte nicht erstellt werden, bitte versuche es später erneut."       
        
        if time.strftime("%p") ==  "AM":
            daytime = False
        elif time.strftime("%p") ==  "PM":
            daytime = True                 
        
        #sonntag ist 0
        if time.strftime("%w") == str(0) and daytime:
            return "Fehler - Preise können Sonntag nachmittags nicht aktualisiert werden."
        
        
        try:
            result = ruebDB.dbrequest('SELECT * FROM turnip_prices WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s', (daytime, author_id))
            
               
            #Check if db entry exists for that day
            if result is None:
                ruebDB.dbcommit("INSERT INTO turnip_prices (price, date, daytime, users_id_fkey) VALUES (%s, NOW()::date, %s, %s)",(turnip_price, daytime, author_id))
        
                logging.info("Preis "+str(turnip_price)+" erfolgreich hinzugefügt.")
                return "Preis "+str(turnip_price)+" erfolgreich hinzugefügt."
            else:
                ruebDB.dbcommit("UPDATE turnip_prices SET price=%s WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s",(turnip_price, daytime, author_id))
                return "Preis geändert auf "+str(turnip_price)
        except ruebDB.ruebDatabaseError:
            return msg.DbError()
#END PRICEADD                  