import discord
import sys
import ruebotActions
import config
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)

client = discord.Client()

callbot1 = "$rübot" 
callbot2 = "$RÜBot"





#Text if user is not registered
notreg_txt = "Benutzer ist nicht registriert. Schreibe '$RÜBot user register' um dich zu registrieren."
msg_wherehelp = "'$RÜBot help' für eine Liste der Befehle"
msg_missingparam = "Fehler - Fehlender Parameter. "+msg_wherehelp
msg_toomanyparam = "Fehler - Zu viele Parameter. "+msg_wherehelp
msg_unknowncommand = "Fehler - unbekannter Befehl. "+msg_wherehelp


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    #Exclude bot's messages
    if message.author == client.user:
        return
    
    #Write userdate into string
    author_id = message.author.id
    author_displayname = str(message.author) 
   
    
    #TODO: Benutzernamen aktualisieren bzw prüfen ob er sich geändert hat
    
    
    
    
    
    #TODO: liste erstellen die durchgegangen wird mit allen möglichen aufrufparametern
    #check for $RÜBot
    if message.content.startswith(callbot1 + ' ') or message.content.startswith(callbot2 + ' '):
        
        #Removes callbot1 or callbot2 from messages
        message_tmp = message.content
        message_tmp = message_tmp[7:]
        logging.info(author_displayname + " schreibt: " + message_tmp)
        print(author_displayname + " schreibt: " + message_tmp)
        
        #Split message into array seperated by spaces
        message_split = message_tmp.split(" ")
        print(message_split)
        
        #HELP  START
        try:
            if message_split[0] == "help" and message_split[1] == "full": 
                helpmsg = open("help_full.txt", "r")
                await message.channel.send("Komplette Hilfe als direktnachricht gesendet!")
                await message.author.send(helpmsg.read())
                return
        except IndexError:
            pass
        try:
            if message_split[0] == "help":
                helpmsg = open("help_brief.txt", "r")
                await message.channel.send(helpmsg.read())
                return
        except IndexError:
            await message.channel.send(msg_missingparam)
            return

        #Help END
        
        #TODO: BUY / SELL, Profittracker. Rüben verfallen nach einer woche.
        
        
        #USER START
       
        try:
            if message_split[0] == "user":
                logging.debug("user")
                #USER REGISTER START
                try: 
                    if message_split[1] == "register" and len(message_split) == 2:
                        logging.debug("register")    
                        #Checks if user is registered and returns result as string
                        await message.channel.send(ruebotActions.userregister(author_id, author_displayname))
                    elif message_split[1] == "register":
                        logging.debug("register - too many parameters")
                        #Too many parameters
                        await message.channel.send(msg_toomanyparam)
                        return
                        
                except IndexError:
                    logging.debug("user - IndexError")
                    pass
                #USER REGISTER END
                
                
                #USER DELETE START
                try:
                    if message_split[1] == "delete" and len(message_split) == 2:
                        logging.debug("USER - DELETE")
                        await message.channel.send(ruebotActions.userdelete(author_id))
                        return
                except IndexError:
                    logging.debug("delete - IndexError")
                    pass
                #USER DELETE END
                
   
                #USER ADDINFO START
                try:
                    if message_split[1] == "addinfo":
                        logging.debug("addinfo")
                        
                        #USER ADDINFO FRUIT START
                        try:
                            if message_split[2] == "fruit" and len(message_split) == 4:
                                logging.debug("fruit")
                                
                                #Fügt Frucht dem Benutzereintrag in der db hinzu
                                await message.channel.send(ruebotActions.addinfoFruit(author_id, message_split[3]))
                                return
                            elif message_split[2] == "fruit" and len(message_split) == 3:
                                #Parameter is missing
                                await message.channel.send(msg_missingparam)
                                return
                            
                            elif message_split[2] == "fruit" and len(message_split) > 4:
                                logging.info(msg_toomanyparam)
                                await message.channel.send(msg_toomanyparam)
                                return
                            
                        except IndexError:
                            pass
                        #USER ADDINFO FRUIT END
                        
                        #USER ADDINFO FC START
                        try:
                            if message_split[2] == "fc" and len(message_split) == 4:
                                logging.debug("USER ADDINFO FC")
                                
                                #Fügt Friendcode dem Benutzereintrag in der db hinzu
                                await message.channel.send(ruebotActions.addinfoFC(author_id, message_split[3]))
                                return
                            elif message_split[2] == "fc" and len(message_split) == 3:
                                #Parameter is missing
                                await message.channel.send(msg_missingparam)
                                return
                            
                            elif message_split[2] == "fc" and len(message_split) > 4:
                                logging.info(msg_toomanyparam)
                                await message.channel.send(msg_toomanyparam)
                                return
                        except IndexError:
                            pass   
                        #USER ADDINFO FC END
                        
                        #USER ADDINFO PIRATE START
                        try:
                            if message_split[2] == "pirate" and len(message_split) == 4:
                                logging.debug("USER ADDINFO PIRATE")
                                
                                #Fügt Friendcode dem Benutzereintrag in der db hinzu
                                await message.channel.send(ruebotActions.addinfoPirate(author_id, message_split[3]))
                                return
                            elif message_split[2] == "pirate" and len(message_split) == 3:
                                #Parameter is missing
                                await message.channel.send(msg_missingparam)
                                return
                            
                            elif message_split[2] == "pirate" and len(message_split) > 4:
                                logging.info(msg_toomanyparam)
                                await message.channel.send(msg_toomanyparam)
                                return
                        except IndexError:
                            pass   
                        
                        #USER ADDINFO PIRATE END
                except IndexError:
                    logging.debug("addinfo - IndexError")
                    pass
                #USER ADDINFO END
                
                #USER DELETEINFO START
                try:
                    if message_split[1] == "deleteinfo":
                        logging.debug("USER - DELETEINFO")
                        
                        #USER DELETEINFO FC START
                        try:
                            if message_split[2] == "fc" and len(message_split) == 3:
                                logging.debug("USER - DELETEINFO - FC")
                                #TODO:
                                #Lösch den Freundescode
                                await message.channel.send(ruebotActions.deleteinfoFC(author_id))
                                return
                            elif message_split[2] == "fc" and len(message_split) > 3:
                                #Parameter is missing
                                logging.info(msg_toomanyparam)
                                await message.channel.send(msg_toomanyparam)
                                return      
                        except IndexError:
                            pass
                        #USER DELETEINFO FRUIT END
                except IndexError:
                    logging.debug("USER DELETEINFO - IndexError")
                    pass
                #USER DELETEINFO END
                
        except IndexError:
            logging.info(msg_missingparam)
            await message.channel.send(msg_missingparam)
            return
        #USER END
        
        
        #PRICE START
        try:
            if message_split[0] == "price" and len(message_split) != 1:
                #PRICE ADD START
                try:
                    if message_split[1] == "add" and len(message_split) == 3:
                        await message.channel.send(ruebotActions.priceAdd(message_split[2], author_id))                      
                        return
                
                    elif message_split[1] == "add" and len(message_split) == 2:
                        logging.info("Fehler - fehlender Parameter <price>")
                        await message.channel.send("Fehler - fehlender Parameter <price>")
                        return
                    else:
                        await message.channel.send(msg_unknowncommand)
                except IndexError:
                    pass
                #PRICE ADD END
                
                
            #Missing parameters
            elif message_split[0] == "price":
                await message.channel.send(msg_missingparam)
                return
        
        except IndexError:
            pass
        #PRICE END
        
        
        #LIST START
        try:
            if message_split[0] == "list" and len(message_split) != 1:
                logging.debug("LIST")
                
                #LIST PRICE START
                try:
                    if message_split[1] == "price" and len(message_split) == 2:
        
                        await message.channel.send(ruebotActions.listPrice())
                        logging.debug("LIST - PRICE")
                        return
                        
                    elif message_split[1] == "price" and len(message_split) > 2:
                        logging.debug("LIST - PRICE: "+msg_toomanyparam)
                        await message.channel.send(msg_toomanyparam)
                        return
                except IndexError:
                    pass
                #LIST PRICE END
                
                #LIST USERS START
                try:
                    if message_split[1] == "users" and len(message_split) == 2:
                        await message.author.send(ruebotActions.listUsers(None))
                        await message.channel.send("Liste als direktnachricht gesendet!")
                        return

                    elif message_split[1] == "users" and len(message_split) > 2:
                        logging.debug("LIST - USERS: "+msg_toomanyparam)
                        await message.channel.send(msg_toomanyparam)
                        return
                except IndexError:
                    pass
                #LIST USERS END
                
                #LIST USER <USERNAME> START
                try:
                    #LIST USER without username parameter
                    if message_split[1] == "user" and len(message_split) == 2:
                        await message.channel.send(ruebotActions.listUsers(author_displayname))
                        return
                    #LIST USER <USERNAME>
                    elif message_split[1] == "user" and len(message_split) == 3:
                        await message.channel.send(ruebotActions.listUsers(message_split[2]))
                        return
                except IndexError:
                    pass
                #LIST USER <USERNAME> END
                
                
        except IndexError:
            pass
        #LIST END
        
        #WENN NICHTS AUFGEFANGEN WURDE
        await message.channel.send('Fehlende Parameter oder unbekannter Command! "$RÜBot help" oder "RÜBot help full" für eine Liste der Kommandos')
        
        
    #Bot aufgerufen, ohne Parameter anzugeben
    elif message.content == callbot1 or message.content == callbot2:
        await message.channel.send('Fehlende Parameter! "$RÜBot help" oder "RÜBot help full" für eine Liste der Kommandos')
    #$RÜBot ende   
        
        
    
try:
    client.run(config.gettoken())
except Exception as e:
    print(e)
    sys.exit(0)
    