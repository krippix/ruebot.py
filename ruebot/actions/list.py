#python native
import logging
import time
import datetime
#part of project
from ruebot.actions import ruebDB
from ruebot import msg
from ruebot import getInfo
#external
from texttable import Texttable
from ruebot.actions.ruebDB import ruebDatabaseError





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

        try:
            final_user_input = ""
            for x in user_input:
                final_user_input = final_user_input + x.lower()
        except Exception as e:
            return e
        
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE LOWER(u.displayname) LIKE %s LIMIT 10",[final_user_input+"%"],)]
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
def pricehistory(author_id, user_input):
    #Lists pricehistory since last monday
    
    #author_id=95480104779526144 #testing
    
    if not getInfo.userexists(author_id):
        logging.info(msg.NotReg())
        return msg.NotReg()
    
    
    #Get last sunday of this week
    try:
        last_sunday = getInfo.lastSunday()
    except Exception as e:
        return e
    
    
    #If no userinput get pricehistory of user typing
    if user_input is None:
        request_id = author_id
    
    
    
    
    #Username was given    
    else:
        
        
        try:
            final_input = ""
            for x in user_input:
                final_input = final_input + x
        except Exception as e:
            return e
        
        
        final_input = final_input.lower()

        try:
            answer_tuple = ruebDB.dbfetchall("SELECT id_pkey FROM users WHERE LOWER(displayname) LIKE %s",[final_input+"%"],)
            logging.info("LIST PRICEHISTORY <USERNAME> : "+str(answer_tuple))
        except ruebDB.ruebDatabaseError:
            logging.error("LIST - USERS: "+ruebDB.ruebDatabaseError)
            return msg.DbError()
        except Exception as e:
            logging.error(e)
            return e
        
        
        if len(answer_tuple) == 0:
            logging.error("Fehler - Keine Benutzer gefunden.")
            return "Fehler - Benutzer hat diese Woche noch keine Rübenpreise registriert."
        
        elif len(answer_tuple) > 1:
            return "Mehr als ein Benutzer gefunden, versuche den Namen + Nummer"
        
       
        request_id = answer_tuple[0]
        
 
    try:
        answer_tuple = ruebDB.dbfetchall("SELECT price, date, daytime FROM turnip_prices WHERE users_id_fkey=%s AND date > %s ORDER BY date ASC, daytime ASC", (request_id, last_sunday))
    except ruebDatabaseError:
        return msg.DbError()
        logging.error(msg.DbError())
    except Exception as e:
        logging.error(e)
        
            
    if answer_tuple is None:
        logging.info("Keine Ergebnisse")
        return "Keine Ergebnisse"
        
        
        
        
        
        
        
    #====================================================================
    i = 0 #Variable for tuple selection
    #k = 0 #Variable for list selection
    #Start with False (AM)
    needet_daytime = False
    answer_list = [[],[]] 
    #start from last monday
    current_date = last_sunday + datetime.timedelta(days=1) #start at monday
    logging.info("current_date: "+str(current_date))
        
    #ANSWER_TUPLE: (price,date,daytime)
  
    logging.debug("LIST PRICEHISTORY - Length answer_tuple: "+str(len(answer_tuple)))
    print(answer_tuple)
    #return
    try:
        
        while i <= len(answer_tuple) - 1 and datetime.date.today() >= answer_tuple[i][1]:
            #logging.debug("test")
            print(i)    
                
            #Is it the expected date?
            if current_date == answer_tuple[i][1]:
                    
                #Is it the expected daytime?
                if needet_daytime == answer_tuple[i][2]:
                    answer_list.append([answer_tuple[i][0], answer_tuple[i][1], answer_tuple[i][2]])
                        
                    #Daytime True or false
                    if answer_tuple[i][2] == True:
                        needet_daytime = False
                            
                        #Next day
                        current_date += datetime.timedelta(days=1)
                       
                    else:
                        needet_daytime = True
        
                    i += 1
                    #k += 1
                    
                #Unexpected daytime
                else:       
                    answer_list.append(['x', current_date, needet_daytime])
                        
                    #change needet daytime to opposite again
                    if needet_daytime == True:
                        needet_daytime = False
                            
                        #Next day
                        current_date += datetime.timedelta(days=1)
                        
                    #Daytime was false, change to next daytime
                    else:
                        needet_daytime = True
                        
                        
                #END DAYTIME?
            #Date is wrong
            else:
                #Place x for wrong date
                answer_list.append(['x', current_date, needet_daytime])
                print(answer_list)
                    
                #Wird nach AM gesucht
                if needet_daytime == True:
                        
                    needet_daytime = False
                    #Next day
                    current_date += datetime.timedelta(days=1)
                    
                else:
                    needet_daytime = True
                    
                   
        
            #END DATE?
        
        
    except Exception as e:
        logging.error(e)
        return e


    #Get full username from request_id
    try:
        answer_displayname = ruebDB.dbfetchall("SELECT displayname FROM users WHERE id_pkey=%s", [request_id],)
    except ruebDatabaseError as e:
        return msg.DbError()
        logging.error(e)
    except Exception as e:
        return e
        logging.error(e)
            
    
    answer = ""+str(answer_displayname[0][0])+" - Rübenpreise seit Montag: \n"
        
        
        
    #price, date, daytime
    for x in answer_list:
            
        try:
            answer = answer + str(x[0]) + "-"
        except IndexError as e:
            pass
        except Exception as e:
            logging.error(e)
            return "Fehler - Konnte Tabelle nicht auswerten!"         
        
    #remove last "-"
    answer = answer[:-1]
        
    return answer
    

    
#LIST PRICEHISTORY <USER END
