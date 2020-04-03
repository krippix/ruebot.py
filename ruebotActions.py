import logging
import ruebDB
import time
from texttable import Texttable

msg_notregistered = "Du musst dich registrieren um diesen Befehl nutzen zu k�nnen: '$R�Bot' user register"

def userregister(author_id, author_displayname):
    
    #Pr�fen ob Benutzer bereits existiert
    if userexists(author_id):
        logging.info("Benutzer existiert bereits.")
        return "Benutzer existiert bereits."
    
    #User wird in datenbank geschrieben             
    else:
        logging.info("Creating new user: "+str(author_displayname)+ " | "+str(author_id))
        
        #Writing user into db
        ruebDB.dbcommit("INSERT INTO users (displayname, id) VALUES (%s, %s)", (author_displayname, author_id))
        return'Benutzer '+author_displayname+' erfolgreich erstellt!'


def userdelete(author_id):
    if userexists(author_id):
        if ruebDB.dbcommit("UPDATE turnip_prices SET users_id_fkey=000000000000000000 WHERE users_id_fkey=%s", (author_id)) is not None:
            logging.info("Benutzer wurde erfolgreich gelöscht!")
            return "Benutzer wurde erfolgreich gelöscht!"
        else:
            logging.error("Benutzer konnte nicht gelöscht werden.")
            return "Fehler - Benutzer konnte nicht gelöscht werden, bitte versuche es später nochmal."
        


def addinfoFruit(author_id, user_input):
    #Add the fruit to your user
    
    
    if not userexists(author_id):
        logging.info(msg_notregistered)
        return msg_notregistered
    
    
    elif user_input.lower() == "penis":
        return 'Haha witzig...'
    
    #list of allowed fruid and what they get converted to
    fruit_dict = {
        "pear": "Birne",
        "birne": "Birne",
        "cherry": "Kirsche",
        "kirsche": "Kirsche",
        "kirschen": "Kirsche",
        "apple": "Apfel",
        "apfel": "Apfel",
        "peach": "Pfirsich",
        "orange": "Orange"  
    }


    try:
        fruit_final = fruit_dict[user_input.lower()]
        print(fruit_final)
        
        ruebDB.dbcommit("UPDATE users SET fruit=%s WHERE id=%s",(fruit_final, author_id))
        return "Frucht erfolgreich hinzugefügt!"
    except KeyError:
        #unknown fruit
        logging.info("Unknown Fruit: "+user_input)
        return "Unbekannte Frucht; Akzeptierte Früchte: Birne, Kirsche, Orange, Apfel und Pfirsich"
    except Exception:    
        logging.error("Fehler bei der Datenbankverbindung!")
        return "Fehler bei der Datenbankverbindung!"


#END addinfoFruit           

def priceList():
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
                
                
    answer_tuple = ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id WHERE t.date=NOW()::date AND daytime=%s",(daytime,))
                
    if answer_tuple is None:
        logging.info("Keine Rübenpreise verfügbar")
        return "Bisher sind keine Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."
                
    answer = ""

    #Testing
    logging.debug("-------------UNBEHANDELT-------------")
    logging.debug(answer_tuple)
    logging.debug("-------------UNBEHANDELT-------------")
    
         
    #Put tuple into single string
    for i in answer_tuple:                    
        answer += str(i)
    
    logging.debug("-------------TUPLE ALS STRING-------------")        
    logging.debug(answer)       
    logging.debug("-------------TUPLE ALS STRING-------------")                   
    
    #Remove first ( and last )
    answer = answer[1:len(answer)-1]
                
    #Split string into list
    answer_list = answer.split(")('")
    
    for i in answer_list:
        print("String: "+i)
    answer_list = [s.replace('\'', '') for s in answer_list]
    answer_list = [s.replace(',', '\t\t') for s in answer_list]
    
    logging.debug("-------------LISTE-------------")
    logging.debug(answer_list)
    logging.debug("-------------LISTE-------------")
    
   
    
    name = ""
    price = ""
    t = Texttable
    
    for i in answer_list:
        print("yeet")
        tmpstring = "dennis,25"
        print("yeet")
        name, price = tmpstring.split(',')
        print("yeet")
        print("Test: "+name+" "+price)
        t.add_row([name, price])

    print(t.draw())
    #Write list into string
    answer_string = ""
    print("yeet?")
    for x in answer_list:
        
        answer_string += x +"\n"
    
    print(answer_string)
    
    return "KÄSEWÜRFEL"
#END PRICELIST

def priceAdd(turnip_price, author_id):
    #add price to db entry of user
    
    
    #check if user exists
    if not userexists(author_id):
        logging.info(msg_notregistered)
        return msg_notregistered
    
    
    #Check if price is viable
    try:
        int(turnip_price)
    except Exception:
        logging.info('"'+turnip_price+'" ist kein Gültiger Preis.')
        return '"'+turnip_price+'" ist kein Gültiger Preis.'
    
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
        
        
        result = ruebDB.dbrequest('SELECT * FROM turnip_prices WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s', (daytime, author_id))            
                   
        #Check if db entry exists for that day
        if result is None:
            ruebDB.dbcommit("INSERT INTO turnip_prices (price, date, daytime, users_id_fkey) VALUES (%s, NOW()::date, %s, %s)",(turnip_price, daytime, author_id))
            logging.info("Preis "+turnip_price+" erfolgreich hinzugefügt.")
            return "Preis "+turnip_price+" erfolgreich hinzugefügt."
        else:
            ruebDB.dbcommit("UPDATE turnip_prices SET price=%s WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s",(turnip_price, daytime, author_id))
            return "Preis geändert auf "+turnip_price            
#END PRICEADD                   
                    

         
#--------------------------------------------------------------------------------
#Check stuff
#--------------------------------------------------------------------------------

def userexists(author_id):
    dbanswer = ruebDB.dbrequest('SELECT id FROM users WHERE id=%s', [author_id])
    
    #Check if db-entry of user exists
    if dbanswer is None:
        return False
    
    return True
