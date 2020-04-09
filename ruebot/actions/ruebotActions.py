#python native
import logging
import time
#part of project
import ruebot.actions.ruebDB
import ruebot.getInfo
import ruebot.msg
#external



def userregister(author_id, author_displayname):
    
    #Pr�fen ob Benutzer bereits existiert
    if ruebot.getInfo.userexists(author_id):
        logging.info("Benutzer existiert bereits.")
        return "Benutzer existiert bereits."
    
    #User wird in datenbank geschrieben             
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        try:
            ruebot.actions.ruebDB.dbcommit("INSERT INTO users (displayname, id_pkey, friendcode, fruits_id_fkey, pirate) VALUES (%s, %s, %s, %s, %s)", (author_displayname, author_id, "<unknown>", 1, "<unknown>"))
            return'Benutzer '+author_displayname+' erfolgreich erstellt!'
            
        except ruebot.actions.ruebDB.ruebDatabaseError:
            return ruebot.msg.DbError()
#END USER REGISTER



def buyrueb(author_id, quantity, price):
    
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
        ruebot.actions.ruebDB.dbcommit("INSERT INTO trade_week (date_sunday, users_id_fkey) VALUES (%s, %s)", (str(date_sunday), author_id))
        logging.info("trade_week für "+str(author_id)+" angelegt")
    except ruebot.actions.ruebDB.ruebDatabaseError:
        logging.error("trade_week anlegen Fehlgeschlagen: "+ruebot.msg.DbError())
        return ruebot.msg.DbError()
    
    
    
    
    #Check if trading_week already exist for that user in this week
    
    #Get current date from db and 
    
    
    

    
    
    
    #try:
        #ruebot.actions.ruebDB.dbcommit("INSERT INTO trade_buys (quantity, price, date, trade_week_id_fkey) VALUES (10, 100, NOW()::date, 1) WHERE ", user_input)
    #except ruebot.actions.ruebDB.ruebDatabaseError:
        #return messages.DbError()
    
    
    
    return "Das könnte ein price add sein amk"
#END BUYRUEB



def userdelete(author_id):
    if ruebot.getInfo.userexists(author_id):
        try:
            ruebot.actions.ruebDB.dbcommit("UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s", [author_id])
            ruebot.actions.ruebDB.dbcommit("DELETE FROM users WHERE id_pkey=%s", [author_id])
            logging.info("Benutzer wurde erfolgreich gelöscht!")
            return "Benutzer wurde erfolgreich gelöscht!"
                
        except ruebot.actions.ruebDB.ruebDatabaseError:
            logging.error("Benutzer konnte nicht gelöscht werden.")
            return ruebot.msg.DbError()
    else:
        return "Benutzer existiert nicht."    
#END USERDELETE



def addinfoFruit(author_id, user_input):
    #Add the fruit to your user
    
    
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    
    elif user_input.lower() == "penis":
        return 'Haha witzig...'
    
    #list of allowed fruid and what they get converted to
    fruit_dict = {
        "cherry": "2",
        "kirsche": "2",
        "kirschen": "2",
        "pear": "3",
        "birne": "3",
        "birnen": "3",
        "peach": "4",
        "pfirsich": "4",
        "arsch": "4",
        "orange": "5",
        "apple": "6",
        "apfel": "6"
    }


    try:
        fruit_final = fruit_dict[user_input.lower()]
        
        ruebot.actions.ruebDB.dbcommit("UPDATE users SET fruits_id_fkey=%s WHERE id_pkey=%s",(fruit_final, author_id))
        return "Frucht erfolgreich hinzugefügt!"
    
    except KeyError:
        #unknown fruit
        logging.info("Unknown Fruit: "+fruit_final)
        return "Unbekannte Frucht; Akzeptierte Früchte: Birne, Kirsche, Orange, Apfel und Pfirsich"  
    except ruebot.actions.ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()         
#END addinfoFruit 



def addinfoFC(author_id, user_input):
    
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    

    #MAKE sw uppercase
    user_input = user_input.upper()

    
    #Cofirms wheather its a FC
    friendcode_check = False
    friendcode_final = "SW-1234-1234-1234"
    
    #"SW-1234-1234-1234"
    if user_input[:3] == "SW-" and len(user_input) == 17:
        
        #Check if numbers between "-"
        #Should be 123412341234
        tmp_test = user_input[3:7]+user_input[8:12]+user_input[13:17]
        #Should be "---"
        tmp_test2 = user_input[2]+user_input[7]+user_input[12]

        #Confirm if format is SW-1234-1234-1234
        if tmp_test.isdigit() and tmp_test2 == "---":
            friendcode_check = True
            friendcode_final = user_input

        else:
            friendcode_check = False
            
    #"1234-1234-1234"
    elif user_input[:4].isdigit() and len(user_input) == 14:

        #should be 123412341234
        tmp_test = user_input[0:4]+user_input[5:9]+user_input[10:14]
        tmp_test2 = user_input[5]+user_input[10]
        
        if tmp_test.isdigit() and tmp_test2 == "--":
            friendcode_check = True
            friendcode_final = "SW-"+user_input
        else:
            friendcode_check = False

    #123412341234
    elif user_input[:12].isdigit() and len(user_input) == 12:
        friendcode_final = "SW-"+user_input[0:4]+"-"+user_input[4:8]+"-"+user_input[8:12]
        friendcode_check = True

    else:
        friendcode_check = False
        return "Wrong Friendcode format"
    
    
    if friendcode_check == False:
        logging.info("Wrong Friendcode format")
        return "Wrong Friendcode format"
    
    #DBconnection
    try:
        ruebot.actions.ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",(friendcode_final, author_id))
        return "Freundescode erfolgreich hinzugefügt!"
    
    except ruebot.actions.ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()        
#END ADDINFO FC



def addinfoPirate(author_id, user_input):
    
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    #make input lowercase
    user_input = user_input.lower()
    
    if user_input == "true":
        pirate_final = True
    elif user_input == "false":
        pirate_final = False
    else:
        return user_input+" ist kein gültiges argument. Akzeptiert werden: true, false."
    
    #commit pirate status to db
    try:
        ruebot.actions.ruebDB.dbcommit("UPDATE users SET pirate=%s WHERE id_pkey=%s",(pirate_final, author_id))
        if pirate_final:
            return ":pirate_flag: Du wurdest als pirat markiert :pirate_flag:"
        else:
            return "Arr, du wurdest als Landratte markiert."
    except ruebot.actions.ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()   
    #END ADDINFOPIRATE
    
    
    
def deleteinfoFC(author_id):
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    try:
        ruebot.actions.ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",("<unknown>",author_id))
        return "Freundescode erfolgreich gelöscht!"
    
    except ruebot.actions.ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()       
#DELETE INFO FC END



def priceAdd(turnip_price, author_id):
    #add price to db entry of user
    
    
    #check if user exists
    if not ruebot.getInfo.userexists(author_id):
        logging.info(ruebot.msg.NotReg())
        return ruebot.msg.NotReg()
    
    
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
            result = ruebot.actions.ruebDB.dbrequest('SELECT * FROM turnip_prices WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s', (daytime, author_id))
            
               
            #Check if db entry exists for that day
            if result is None:
                ruebot.actions.ruebDB.dbcommit("INSERT INTO turnip_prices (price, date, daytime, users_id_fkey) VALUES (%s, NOW()::date, %s, %s)",(turnip_price, daytime, author_id))
        
                logging.info("Preis "+str(turnip_price)+" erfolgreich hinzugefügt.")
                return "Preis "+str(turnip_price)+" erfolgreich hinzugefügt."
            else:
                ruebot.actions.ruebDB.dbcommit("UPDATE turnip_prices SET price=%s WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s",(turnip_price, daytime, author_id))
                return "Preis geändert auf "+str(turnip_price)
        except ruebot.actions.ruebDB.ruebDatabaseError:
            return ruebot.msg.DbError()
#END PRICEADD                   





#---------------------------------------------------------------------------------------------------------------------

