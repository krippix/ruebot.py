#python native
import logging
import time
#part of project
import ruebDB
import getInfo
import msg
#external
from texttable import Texttable


def userregister(author_id, author_displayname):
    
    #Pr�fen ob Benutzer bereits existiert
    if getInfo.userexists(author_id):
        logging.info("Benutzer existiert bereits.")
        return "Benutzer existiert bereits."
    
    #User wird in datenbank geschrieben             
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        try:
            ruebDB.dbcommit("INSERT INTO users (displayname, id_pkey, friendcode, fruits_id_fkey, pirate) VALUES (%s, %s, %s, %s, %s)", (author_displayname, author_id, "<unknown>", 1, "<unknown>"))
            return'Benutzer '+author_displayname+' erfolgreich erstellt!'
            
        except ruebDB.ruebDatabaseError:
            return msg.DbError()
#END USER REGISTER



def buyrueb(author_id, quantity, price):
    
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    
    #Check if Number of Rüb is dividable by 10
    if int(quantity) % 10 != 0:
        return "Rüben konnen nur in 10er Schritten gekauft werden!"
    
    if int(price) < 1 or int(price) > 1000:
        return "Price muss zwischen 1 und 1000 liegen!"
    
    
    #Get current sunday
    date_sunday = getInfo.FirstDayOfWeek(time.strftime("%Y-%m-%d"))
    
    
    
    #TODO: Prüfen ob es für diese Woche bereits angelegt wurde
    #Kalenderwoche in Python handlen SQL ist zu umständlich.
    # NOW()::date bleibt denke ich erstmal. Obwohl die Zeit bei rübot liegen sollte.
    
    #TODO: nur durchlassen wenn die Woche noch nicht existiert
    #Anlegen einer trade_week /es wird angenommen dass noch keine existiert
    try:
        ruebDB.dbcommit("INSERT INTO trade_week (date_sunday, users_id_fkey) VALUES (%s, %s)", (str(date_sunday), author_id))
        logging.info("trade_week für "+str(author_id)+" angelegt")
    except ruebDB.ruebDatabaseError:
        logging.error("trade_week anlegen Fehlgeschlagen: "+msg.DbError())
        return msg.DbError()
    
    
    
    
    #Check if trading_week already exist for that user in this week
    
    #Get current date from db and 
    
    
    

    
    
    
    #try:
        #ruebDB.dbcommit("INSERT INTO trade_buys (quantity, price, date, trade_week_id_fkey) VALUES (10, 100, NOW()::date, 1) WHERE ", user_input)
    #except ruebDB.ruebDatabaseError:
        #return messages.DbError()
    
    
    
    return "Das könnte ein price add sein amk"
#END BUYRUEB



def userdelete(author_id):
    if getInfo.userexists(author_id):
        try:
            ruebDB.dbcommit("UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s", [author_id])
            ruebDB.dbcommit("DELETE FROM users WHERE id_pkey=%s", [author_id])
            logging.info("Benutzer wurde erfolgreich gelöscht!")
            return "Benutzer wurde erfolgreich gelöscht!"
                
        except ruebDB.ruebDatabaseError:
            logging.error("Benutzer konnte nicht gelöscht werden.")
            return msg.DbError()
    else:
        return "Benutzer existiert nicht."    
#END USERDELETE



def addinfoFruit(author_id, user_input):
    #Add the fruit to your user
    
    
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    
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
        
        ruebDB.dbcommit("UPDATE users SET fruits_id_fkey=%s WHERE id_pkey=%s",(fruit_final, author_id))
        return "Frucht erfolgreich hinzugefügt!"
    
    except KeyError:
        #unknown fruit
        logging.info("Unknown Fruit: "+fruit_final)
        return "Unbekannte Frucht; Akzeptierte Früchte: Birne, Kirsche, Orange, Apfel und Pfirsich"  
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return msg.DbError()         
#END addinfoFruit 



def addinfoFC(author_id, user_input):
    
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    

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
        ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",(friendcode_final, author_id))
        return "Freundescode erfolgreich hinzugefügt!"
    
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return msg.DbError()        
#END ADDINFO FC



def addinfoPirate(author_id, user_input):
    
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
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
        ruebDB.dbcommit("UPDATE users SET pirate=%s WHERE id_pkey=%s",(pirate_final, author_id))
        if pirate_final:
            return ":pirate_flag: Du wurdest als pirat markiert :pirate_flag:"
        else:
            return "Du bist wieder ein ehrwürdiger Bürger! ⁿᵃʲᵃ"
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return msg.DbError()   
    #END ADDINFOPIRATE
    
    
    
def deleteinfoFC(author_id):
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    try:
        ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",("<unknown>",author_id))
        return "Freundescode erfolgreich gelöscht!"
    
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return msg.DbError()       
#DELETE INFO FC END



def priceAdd(turnip_price, author_id):
    #add price to db entry of user
    
    
    #check if user exists
    if not getInfo.userexists(author_id):
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



def listPrice(author_id):
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
#END PRICELIST




def listUsers(user_input):
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


#---------------------------------------------------------------------------------------------------------------------

