#python native
import logging
import time
#part of project
import ruebot
from ruebot import ruebDB
#external
def buy(author_id, quantity, price):
    
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    
    #Check if Number of Rüb is dividable by 10
    if int(quantity) % 10 != 0:
        return "Rüben konnen nur in 10er Schritten gekauft werden!"
    
    if int(price) < 1 or int(price) > 1000:
        return "Preis muss zwischen 1 und 1000 liegen!"
    
    
    #Get current sunday
    try:
        date_sunday = ruebot.getInfo.lastSunday(time.strftime("%Y-%m-%d"))
    except Exception as e:
        logging.error("BUY: "+str(e))
    
    
    
    #Check if current week has been created
    try:
        answer_tuple = ruebDB.dbfetchall("SELECT id_pkey from trade_week WHERE date_sunday = %s AND users_id_fkey = %s", (date_sunday,author_id))
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()
    
    #Check if there is more than one result (that should !NEVER! happen)
    
    
    
    
    # NOW()::date bleibt denke ich erstmal. Obwohl die Zeit bei rübot liegen sollte.
    
    #TODO: nur durchlassen wenn die Woche noch nicht existiert
    #Anlegen einer trade_week /es wird angenommen dass noch keine existiert
    try:
        ruebDB.dbcommit("INSERT INTO trade_week (date_sunday, users_id_fkey) VALUES (%s, %s)", (str(date_sunday), author_id))
        logging.info("trade_week für "+str(author_id)+" angelegt")
    except ruebDB.ruebDatabaseError:
        logging.error("trade_week anlegen Fehlgeschlagen: "+ruebot.msg.DbError())
        return ruebot.msg.DbError()
    
    
    
    
    #Check if trading_week already exist for that user in this week
    
    #Get current date from db and 
    
    
    

    
    
    
    #try:
        #ruebot.ruebDB.dbcommit("INSERT INTO trade_buys (quantity, price, date, trade_week_id_fkey) VALUES (10, 100, NOW()::date, 1) WHERE ", user_input)
    #except ruebot.ruebDB.ruebDatabaseError:
        #return messages.DbError()
    
    
    
    return "Das könnte ein price add sein amk"
#END BUYRUEB

