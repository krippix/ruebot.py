#python native
import logging
import time
import datetime
#part of project
from ruebot import ruebDB
from ruebot import msg
from ruebot import getInfo
#external
from texttable import Texttable
from ruebot.ruebDB import ruebDatabaseError





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
        logging.error("LIST PRICES: Couldn't retrieve time!")
        return "Fehler - Zeit konnte nicht abgerufen werden, bitte versuche es später erneut."           
                
    
    #If sunday, display lowest prices first
    if time.strftime("%w") == str(0):
        order = "ASC"
    else:
        order = "DESC"  
    
    try:
        #Retrieve whether user is marked as pirate
        answer_tuple = ruebDB.dbrequest("SELECT pirate FROM users WHERE id_pkey=%s", [author_id],)
        logging.info(answer_tuple)
        
        
        
        
        #Check if pirate is true
        if answer_tuple[0] == 'true':
            logging.debug("PIRATE = TRUE")
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id_pkey WHERE t.date=NOW()::date AND daytime=%s AND pirate='true' ORDER BY t.price "+order,(daytime,))]
            tablename = ":pirate_flag:Piratendaten:pirate_flag:: "
            
            if len(answer_tuple) == 0:
                logging.info("Keine Rübenpreise verfügbar")
                return "Bisher sind keine :pirate_flag:-Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."
        
        
        

    except ruebDB.ruebDatabaseError:
        return msg.DbError()
    
    except TypeError:
        pass
        
    finally:
        #Regular users:
        answer_tuple = [r for r in ruebDB.dbfetchall("SELECT u.displayname, t.price FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id_pkey WHERE t.date=NOW()::date AND daytime=%s AND NOT pirate='true' ORDER BY t.price "+order,(daytime,))]
        tablename = "Nomale Daten: "
        if len(answer_tuple) == 0:
            logging.info("Keine Rübenpreise verfügbar")
            return "Bisher sind keine Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu."
    #except TypeError:

    
    
    #prints input into string
    t = Texttable()
    t.add_row(["Benutzer","Preis"])
    
    for x in answer_tuple:
        t.add_row(x)
    
    answer = t.draw()
    

    
    return tablename+"\n```\n"+answer+"```"
#END LIST PRICE



#LIST USER | LIST USER <USERNAME> START
def user(user_input):
    
    #TODO: Eigentliche Abfrage mit User-ID vornehmen und Mention einbauen
    
    reqknown = False
    
        
    #user is given as mention
    try:
        #@<username> was given Format: <@!280098940156772352>
        if user_input[0][0:2] == "<@" and user_input[0][-1] == ">" and not reqknown:
            request_id = ''.join(i for i in user_input[0] if i.isdigit())
            logging.debug("request_id: "+request_id)
            reqknown = True
    
    except Exception as e:
        logging.info("*LIST PRICEHISTORY: "+str(e))
        pass
    

    #GET USER_ID FROM userinput string
    if reqknown == False:
        try:
            final_user_input = ""
            for x in user_input:
                final_user_input = final_user_input + x.lower()
        except Exception as e:
            logging.error("LIST USER: "+str(e))
            return "Fehler bei der Abfrage."
        try:
            answer_tuple = [r for r in ruebDB.dbfetchall("SELECT id_pkey FROM users WHERE LOWER(displayname) LIKE %s LIMIT 10",[final_user_input+"%"],)]
        except ruebDB.ruebDatabaseError:
            logging.error("LIST - USERS: "+str(ruebDB.ruebDatabaseError))
            return msg.DbError()
        
        
        #check if there was no results
        if len(answer_tuple) == 0:
            return "Keine Benutzer gefunden."
        
        #Check if multiple results
        elif len(answer_tuple) > 1:
            return "Mehr als ein Benutzer gefunden, bitte verfeinere deine Suche."
        
        #convert result into string
        elif len(answer_tuple) == 1:
            request_id = answer_tuple[0]
    #END GET USER_ID
    
    
    #Get user from id    
    
    try:
        answer_tuple = ruebDB.dbfetchall("SELECT u.displayname, f.fruit, u.friendcode, u.pirate FROM users AS u JOIN fruits AS f ON f.id_pkey = u.fruits_id_fkey WHERE u.id_pkey=%s" , [request_id],)
    except ruebDB.ruebDatabaseError as e:
        logging.error("LIST USERS: "+str(e))
        return msg.DbError()
    
    
    if len(answer_tuple) == 0:
        logging.error("LIST USERS - Keine Benutzer gefunden.")
        return msg.noUser()
    
    
    #prints input into string
    try:
        answer = ">>> "
        answer += "**"+str(answer_tuple[0][0])+"**" + "\n"
        answer += "Frucht: "+str(answer_tuple[0][1]) + "\n"
        answer += "Freundescode: "+str(answer_tuple[0][2]) + "\n"
        answer += "Pirat: "+str(answer_tuple[0][3]) + "\n"
    except Exception as e:
        logging.error(e)
    
    return answer         
#LIST USER <USERNAME> END    



#LIST PRICEHISTORY <USER>
def pricehistory(author_id, user_input):
    #Lists pricehistory since last monday
    #TODO: Add Sunday-Sellprice
    
    #Get last sunday of this week
    try:
        last_sunday = getInfo.lastSunday()
    except Exception as e:
        return e
    
    
    #Variable to check if request_id has been determined
    reqknown = False
    
    if len(user_input) == 0:
        request_id = author_id
        reqknown = True
    
    try:
        #@<username> was given Format: <@!280098940156772352>
        if user_input[0][0:2] == "<@" and user_input[0][-1] == ">" and not reqknown:
            request_id = ''.join(i for i in user_input[0] if i.isdigit())
            logging.debug("request_id: "+request_id)
            reqknown = True
    
    except Exception as e:
        logging.info("*LIST PRICEHISTORY: "+str(e))
        pass
    
    #Get Userid from user_input
    if reqknown == False:
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
            return msg.noUser()
        
        elif len(answer_tuple) > 1:
            return "Mehr als ein Benutzer gefunden, bitte verfeinere deine Suche."
        
       
        request_id = answer_tuple[0]
        
    
    #Check if requestID exists
    if not getInfo.userexists(request_id):
        logging.info(msg.NotReg())
        return "Der angefragte Benutzer existiert nicht."
    
    #Get Get known prices of user with request_id
    try:
        answer_tuple = ruebDB.dbfetchall("SELECT price, date, daytime FROM turnip_prices WHERE users_id_fkey=%s AND date > %s ORDER BY date ASC, daytime ASC", (request_id, last_sunday))
    except ruebDatabaseError:
        return msg.DbError()
        logging.error(msg.DbError())
    except Exception as e:
        return e
        
            
    if answer_tuple is None:
        logging.info("Keine Ergebnisse")
        return "Keine Ergebnisse"
  

    #====================================================================
    i = 0 #Variable for tuple selection
   
    #Start with False (AM)
    needet_daytime = False
    answer_list = [[],[]] 
    #start from last monday
    try:
        current_date = last_sunday + datetime.timedelta(days=1) #start at monday
    except Exception as e:
        logging.error(e)
    
    
    logging.info("LIST PRICEHISTORY - current_date: "+str(current_date))
        
    #ANSWER_TUPLE: (price,date,daytime)
  
    logging.debug("LIST PRICEHISTORY - Length answer_tuple: "+str(len(answer_tuple)))
    logging.debug("LIST PRICEHISTORY - Content answer_tuple: "+str(answer_tuple))
    #return
    
    
    #Combine Answer into a string, left out days will be replaced with x
    try: 
        while i <= len(answer_tuple) - 1 and datetime.date.today() >= answer_tuple[i][1]:
            #logging.debug("test")  
                
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
    #End Stringbuilder

    
    #Get Saleprice of Sunday
    try:
        price_sunday = ruebDB.dbrequest("SELECT price FROM turnip_prices WHERE users_id_fkey=%s AND date=%s", (request_id, last_sunday))
    except ruebDatabaseError as e:
        return msg.DbError()
        logging.error(e)
    except Exception as e:
        return e
    #End get Saleprice
    
    
    
    #Get full username from request_id
    try:
        answer_displayname = ruebDB.dbfetchall("SELECT displayname FROM users WHERE id_pkey=%s", [request_id],)
    except ruebDatabaseError as e:
        return msg.DbError()
        logging.error(e)
    except Exception as e:
        return e
        logging.error(e)
            
    
    #Build Answer string
    answer = ">>> **"+str(answer_displayname[0][0])+"** - Rübenpreise\n" 
    
    #If sunday price was given:
    if price_sunday is not None:
        answer += "Sonntag: "+ str(price_sunday[0])+"\n" 
        
    answer += "Seit Montag: "
    
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
#LIST PRICEHISTORY <USER> END
