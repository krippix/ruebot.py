import logging
import ruebDB
import time
from texttable import Texttable
from ruebDB import ruebDatabaseError

msg_notregistered = "Du musst dich registrieren um diesen Befehl nutzen zu können: '$RÜBot user register'"
msg_databaseError = "Fehler bei der Datenbankverbindung - Versuche es später nochmal."

def userregister(author_id, author_displayname):
    
    #Pr�fen ob Benutzer bereits existiert
    if userexists(author_id):
        logging.info("Benutzer existiert bereits.")
        return "Benutzer existiert bereits."
    
    #User wird in datenbank geschrieben             
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        try:
            if ruebDB.dbcommit("INSERT INTO users (displayname, id_pkey, friendcode, fruits_id_fkey, pirate) VALUES (%s, %s, %s, %s, %s)", (author_displayname, author_id, "<unknown>", 1, "<unknown>")) is not None:
                return'Benutzer '+author_displayname+' erfolgreich erstellt!'
            else:
                return "Fehler - Benutzer konnte nicht erstellt werden, bitte versuche es später nochmal."
        except ruebDatabaseError:
            return msg_databaseError

def userdelete(author_id):
    if userexists(author_id):
        try:
            ruebDB.dbcommit("UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s", [author_id])
            ruebDB.dbcommit("DELETE FROM users WHERE id_pkey=%s", [author_id])
            logging.info("Benutzer wurde erfolgreich gelöscht!")
            return "Benutzer wurde erfolgreich gelöscht!"
                
        except ruebDatabaseError:
            logging.error("Benutzer konnte nicht gelöscht werden.")
            return msg_databaseError
    else:
        return "Benutzer existiert nicht."    

def addinfoFruit(author_id, user_input):
    #Add the fruit to your user
    
    
    if not userexists(author_id):
        logging.info(msg_notregistered)
        return msg_notregistered
    
    
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
    except ruebDatabaseError as e:
        logging.error(e)
        return msg_databaseError
         
#END addinfoFruit 

def addinfoFC(author_id, user_input):
    
    if not userexists(author_id):
        logging.info(msg_notregistered)
        return msg_notregistered
    

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
    
    except ruebDatabaseError as e:
        logging.error(e)
        return msg_databaseError        


def priceAdd(turnip_price, author_id):
    #add price to db entry of user
    
    
    #check if user exists
    if not userexists(author_id):
        logging.info(msg_notregistered)
        return msg_notregistered
    
    
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
        if time.strftime("%w") == 0:
            return "Fehler - Preise können Sonntags nicht aktualisiert werden."
        
        
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
        except ruebDatabaseError:
            return msg_databaseError
#END PRICEADD                   


def listPrice():
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
        answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id_pkey WHERE t.date=NOW()::date AND daytime=%s ORDER BY t.price DESC",(daytime,))]
        if len(answer_tuple) == 0:
            logging.info("Keine Rübenpreise verfügbar")
            return "Bisher sind keine Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."
    
    except ruebDatabaseError:
        return msg_databaseError
    
    #prints input into string
    t = Texttable()
    t.add_row(["Benutzer","Preis"])
    
    for x in answer_tuple:
        t.add_row(x)
    
    answer = t.draw()
    
    print(answer)
    
    return "```\n"+answer+"```"
#END PRICELIST


def listUsers(user_input):
    #pass None if all users should be displayed
    if user_input is None:
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE NOT (u.id_pkey = 0 )",(),)]
        except ruebDatabaseError:
            logging.error("LIST - USERS: "+ruebDatabaseError)
            return msg_databaseError
        
    
        if len(answer_tuple) == 0:
            logging.error("Fehler - Keine Benutzer gefunden.")
            return "Fehler - Keine Benutzer gefunden."
    #Username is defined
    else:

        user_input = user_input.lower()
        
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE LOWER(u.displayname) LIKE %s",[user_input+"%"],)]
        except ruebDatabaseError:
            logging.error("LIST - USERS: "+ruebDatabaseError)
            return msg_databaseError
        
    
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
    
#--------------------------------------------------------------------------------
#Check stuff
#--------------------------------------------------------------------------------

def userexists(author_id):
    
    try:
        dbanswer = ruebDB.dbrequest('SELECT id_pkey FROM users WHERE id_pkey=%s', [author_id])
    except ruebDatabaseError:
        return msg_databaseError
    
    #Check if db-entry of user exists
    if dbanswer is None:
        return False
    
    return True
