import discord
import configparser
import sys
import logging
import logging.config
import time
import os
import ruebDB
import ruebotActions



client = discord.Client()

callbot1 = "$rübot" 
callbot2 = "$RÜBot"

#name of inifile
inifile = 'config.ini'

#name of section for token
section = 'botconfig'

#name of token
tokenname = 'token'

#Text if user is not registered
notreg_txt = "Benutzer ist nicht registriert. Schreibe '$RÜBot user register' um dich zu registrieren."


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    #Exclude bot's messages
    if message.author == client.user:
        return
    
    #check for $RÜBot
    #TODO: liste erstellen die durchgegangen wird mit allen möglichen aufrufparametern
    
    if message.content.startswith(callbot1 + ' ') or message.content.startswith(callbot2 + ' '):
        
        message_tmp = message.content
        message_tmp = message_tmp[7:]
        print('Nachricht ohne $RÜBot: ' + message_tmp)
        
        #Split message into array seperated by spaces
        message_split = message_tmp.split(" ")
        
        #userdate into strings
        author_id = message.author.id
        author_displayname = str(message.author)
        #TEST
        #author_id = "123456789"
        #author_displayname = ""
        
        #Help
        if message_split[0] == "help":
            helpmsg = open("help.txt", "r")
            await message.channel.send(helpmsg.read())
            return
    
    #gibt empfangenen text aus
            
        
        #Help END
        
        
        #user commands
        if message_split[0] == "user" and len(message_split) >= 2:
            #TODO: Benutzernamen aktualisieren bzw prüfen ob er sich geändert hat
            
            #user registrieren: $RÜBot user register
            if message_split[1] == "register" and len(message_split) == 2:
                
                await message.channel.send(ruebotActions.userregister(author_id, author_displayname))
            
            elif message_split[1] == "register" and len(message_split) > 2:
                print("user register: too many parameters")
                await message.channel.send('Zu viele Parameter! Registrierung abgebrochen.')
                return
            #END USER REGISTER
            
            #user addinfo - 3 params
            #USER HAS TO BE REGISTERED
            if userexists(author_id):
                #user addinfo <...>
                if message_split[1] == "addinfo" and len(message_split) == 4:
                    #Native fruit
                    if message_split[2] == "native":
                        #allowed fruits
                        fruit = ['pear', 'cherry', 'orange', 'apple', 'peach', 'birne', 'kirsche', 'kirschen', 'orange', 'apfel', 'pfirsich']
                        
                        #check if userinput exists
                        if message_split[3].lower() in fruit:
                            final_fruit = message_split[3]
                            
                            #Please don't hit me for this block
                            if final_fruit == "pear" or final_fruit == "birne":
                                final_fruit = "Birne"
                            if final_fruit == "cherry" or final_fruit == "kirsche":
                                final_fruit = "Kirsche"
                            if final_fruit == "orange" or final_fruit == "orange":
                                final_fruit = "Orange"
                            if final_fruit == "apple" or final_fruit == "apfel":
                                final_fruit = "Apfel"
                            if final_fruit == "peach" or final_fruit == "Pfirsich":
                                final_fruit = "Pfirsich"
                            
                        
                            dbcommit("UPDATE users SET fruit=%s WHERE id=%s", (final_fruit, author_id))
                            return
                        else:
                            print("Unbekannte Frucht; Akzeptierte Früchte: Birne, Kirsche, Orange, Apfel und Pfirsich")
                            await message.channel.send('Unbekannte Frucht: akzeptierte Früchte: Birne, Kirschen, Orange, Apfel und Pfirsich')
                            return
                    #ENDE NATIVE FRUCHT   
                   
                elif len(message_split) > 4:
                    await message.channel.send('Zu viele Parameter!')
                #ENDE ADDINFO 
                
            else: #user doesent exist
                print(notreg_txt)
                await message.channel.send(notreg_txt)
                return
            #END USER ADDINFO
            
            
            
        #check if nothing after "user"
        elif message_split[0] == "user" and len(message_split) == 1:
            await message.channel.send('Fehlende Parameter! "$RÜBot help" für eine Liste der Kommandos')
            return
        #ENDE USER COMMANDS
        
        
        
        
        #price commands
        if message_split[0] == "price" and len(message_split) >= 2:
            if message_split[1] == "list" and len(message_split) == 2:
                
                #vor oder nachmittag
                if time.strftime("%p"):
                            time_ampm = time.strftime("%p") 
                            
                            #Vormittag = 0 
                            if time_ampm == "AM":
                                daytime = False
                            elif time_ampm == "PM":
                                daytime = True
                
                
                answer_tuple = dbfetchall("SELECT t.price, u.displayname FROM turnip_prices AS t JOIN users AS u ON t.users_id_fkey = u.id WHERE t.date=NOW()::date AND daytime=%s",(daytime,))
                
                if answer_tuple is None:
                    print("Keine Rübenpreise verfügbar")
                    await message.channel.send("Bisher sind keine Rübenpreise eingetragen.\nFüge deinen aktuellen Preis mit '$RÜBot price add <preis>' hinzu.")
                    return 
                
                answer = ""
                #TODO: handle nonoe
                #Testing
                print("unbehandelte liste:")
                print(answer_tuple)
         
                #Put tuple into single string
                for i in answer_tuple:                    
                    answer += str(i) + "$"
                answer = answer[:len(answer)-1]                
                
                #Remove unwanted chars    
                bad_chars = ["(", ")", "'", "*"] 
                answer = ''.join(i for i in answer if not i in bad_chars) 
                
                #Split string into list
                answer_list = answer.split("$")
         
                await message.channel.send(answer_list)
                print(answer_list)
                return
  
            #check for 3 arguments
            if len(message_split) == 3:
                if message_split[1] == "add" and userexists(author_id):
                    turnip_price = int(message_split[2])
                    #TODO: dont allow on sunday
                    #attempt to convert price to int
                    try:
                        int(turnip_price)
                    except Exception:
                        await message.channel.send('"'+turnip_price+'" ist kein Gültiger Preis.')
                        return
                    
                    #Check if turnip price is in allowed range
                    if turnip_price < 1 or turnip_price > 1000:
                        await message.channel.send('Der Preis muss zwischen 1 und 1000 liegen!')
                    else:
                        print("komme ich hier an?")
                        if time.strftime("%p"):
                            time_ampm = time.strftime("%p") 
                            
                            #Vormittag = 0 
                            if time_ampm == "AM":
                                daytime = False
                            elif time_ampm == "PM":
                                daytime = True
                            
                            #Check if db entry exists for that day
                            result = dbrequest('SELECT * FROM turnip_prices WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s', (daytime, author_id))
                            if result is None:
                                print()
                                dbcommit("INSERT INTO turnip_prices (price, date, daytime, users_id_fkey) VALUES (%s, NOW()::date, %s, %s)",(turnip_price, daytime, author_id))
                                return
                            elif result is not None:
                                dbcommit("UPDATE turnip_prices SET price=%s WHERE date=NOW()::date AND daytime=%s AND users_id_fkey=%s",(turnip_price, daytime, author_id))
                                return
                            
                            
                            
                        else:
                            print("Time couldnt be retrieved")
                            await message.channel.send('Fehler - Versuche es später nocheinmal')
                            return
                elif not userexists(author_id):
                    print(notreg_txt)
                    await message.channel.send(notreg_txt)
                    return
            else:
                print("Syntax error!")               
                await message.channel.send('Syntax error!')
                return
                #TODO: hier genauer werden        
                        
                        
            #ENDE PRICE ADD           
        #check if missing parameters
        elif message_split[0] == "price" and len(message_split) == 1:
            await message.channel.send('Fehlende Parameter! "$RÜBot help" für eine Liste der Kommandos')
        #ENDE PRICE COMMANDS
        
        
        
    
    #Bot aufgerufen, ohne Parameter anzugeben
    elif message.content == callbot1 or message.content == callbot2:
        await message.channel.send('Fehlende Parameter! "$RÜBot help" für eine Liste der Kommandos')

    
#checks if user is registered in db


#TODO Check if inifile is present
def checkini(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    
    return True #True = it works


#pull token from ini
def gettoken():
    if not checkini(inifile):
        print(inifile +" is missing.")
        sys.exit(0)
    
    config = configparser.ConfigParser()
    config.read(inifile)
    
    #check for the part i actually need lel
    #Check if [botconfig] is in ini
    if 'botconfig' not in config:
        print("section '["+section+"]' missing. Delete ini and restart to create new one.")
        sys.exit(0)

    token = config[section][tokenname]   
    
    #check if token is empty
    if token == '\'\'':
        print("Your token seems to be missing, check "+inifile)
        sys.exit(0)
    elif token == tokenname:
        print('"'+tokenname+'" in "['+section+'] seems to be missing, delete or rename '+inifile+' to regenerate')
        sys.exit(0)
    elif not token[0] == '\'' or not token[len(token)-1] == '\'':
        print("Invalid format, make sure your token is surrounded by ''")
        sys.exit(0)
    
    
    #Token is here and seems to be ok :D
    #remove '' from token
    token = token[1:len(token)-1]
    print('Attempting connection token: ' + token)
    
    return token

    
try:
    client.run(gettoken())
except Exception as e:
    print(e)
    sys.exit(0)
    