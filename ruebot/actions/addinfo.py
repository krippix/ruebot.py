#python native
import logging
#part of project
from ruebot import ruebDB
import ruebot.getInfo
#external


def fruit(author_id, user_input):
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

        ruebDB.dbcommit("UPDATE users SET fruits_id_fkey=%s WHERE id_pkey=%s",(fruit_final, author_id))
        return "Frucht erfolgreich hinzugefügt!"
    
    except KeyError:
        #unknown fruit
        logging.info("Unknown Fruit: "+str(user_input))
        return "Unbekannte Frucht; Akzeptierte Früchte: Birne, Kirsche, Orange, Apfel und Pfirsich"  
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()         
#END addinfoFruit 



def friendcode(author_id, user_input):
    
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
        ruebDB.dbcommit("UPDATE users SET friendcode=%s WHERE id_pkey=%s",(friendcode_final, author_id))
        return "Freundescode erfolgreich hinzugefügt!"
    
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()        
#END ADDINFO FC



def pirate(author_id, user_input):
    
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
        return "'"+user_input+"' ist kein gültiges argument. Akzeptiert werden: true, false."
    
    #commit pirate status to db
    try:
        ruebDB.dbcommit("UPDATE users SET pirate=%s WHERE id_pkey=%s",(pirate_final, author_id))
        if pirate_final:
            return ":pirate_flag: Du wurdest als pirat markiert :pirate_flag:"
        else:
            return "Arr, du wurdest als Landratte markiert."
    except ruebDB.ruebDatabaseError as e:
        logging.error(e)
        return ruebot.msg.DbError()   
    #END ADDINFOPIRATE