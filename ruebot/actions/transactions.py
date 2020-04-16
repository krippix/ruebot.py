"""
def buy(author_id, quantity, price):
    
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    
    #Check if Number of Rüb is dividable by 10
    if int(quantity) % 10 != 0:
        return "Rüben konnen nur in 10er Schritten gekauft werden!"
    
    if int(price) < 1 or int(price) > 1000:
        return "Price muss zwischen 1 und 1000 liegen!"
    
    
    #Get current sunday
    #date_sunday = ruebot.getInfo.FirstDayOfWeek(time.strftime("%Y-%m-%d"))
    
    
    
    #TODO: Prüfen ob es für diese Woche bereits angelegt wurde
    #Kalenderwoche in Python handlen SQL ist zu umständlich.
    # NOW()::date bleibt denke ich erstmal. Obwohl die Zeit bei rübot liegen sollte.
    
    #TODO: nur durchlassen wenn die Woche noch nicht existiert
    #Anlegen einer trade_week /es wird angenommen dass noch keine existiert
    try:
        ruebot.ruebDB.dbcommit("INSERT INTO trade_week (date_sunday, users_id_fkey) VALUES (%s, %s)", (str(date_sunday), author_id))
        logging.info("trade_week für "+str(author_id)+" angelegt")
    except ruebot.ruebDB.ruebDatabaseError:
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
"""
