#python native
import logging
import sys
#part of project
import ruebot.config
from ruebot.actions import list
from ruebot.actions import addinfo
from ruebot.actions import deleteinfo
from ruebot.actions import user
from ruebot.actions import price
from ruebot import msg
from ruebot import getInfo
#external
import discord #discord.py


#SET logginglevel
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)

#Variable for calling the bot
callbot = "$rübot" 

client = discord.Client()


#Text if user is not registered
notreg_txt = "Benutzer ist nicht registriert. Schreibe '$RÜBot user register' um dich zu registrieren."
msg_wherehelp = "'$RÜBot help' für eine Liste der Befehle"

msg_unknowncommand = "Fehler - unbekannter Befehl. "+msg_wherehelp



#TODO: userid über funktion aus @mention extrahieren.
#TODO: userid kann verschieden Anfangen! <@! <@& <@


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    #Exclude bot's msg
    if message.author == client.user:
        return
    
    #Write userdate into string
    author_id = message.author.id
    author_displayname = str(message.author) 
    
    
    #check for if bot is actually called $RÜBot
    if message.content.lower().startswith(callbot + ' '):
        
        #Check if username was changed since last message
        if getInfo.userexists(author_id):
            logging.info("Checking if username was changed.")
            logging.info(getInfo.updateDisplaynames(author_displayname, author_id))
            
        
        #Removes callbot from message
        message_tmp = message.content
        message_tmp = message_tmp[len(callbot)+1:]
        logging.info(author_displayname + " wrote: " + message_tmp)
        
        #Split message into array seperated by spaces
        message_split = message_tmp.split(" ")
        logging.debug("Message as list: "+str(message_split))
        
        
        #HELP  START
        try:
            if message_split[0] == "help" and message_split[1] == "full": 
                #helpmsg = open("help_full.txt", "r")
                await message.channel.send("Komplette Hilfe als direktnachricht gesendet!")
                await message.author.send(msg.help_full())
                return
        except IndexError:
            pass
        try:
            if message_split[0] == "help":
                await message.channel.send(msg.help_brief())
                return
        except IndexError:
            pass
        #Help END
        
        
        
        #TODO: SELL, Profittracker. Rüben verfallen nach einer woche.
        
        
        """
        #TODO: BUY START
        try:
            if message_split[0] == "buy" and message_split[1].isdigit() and message_split[2] == "at" and message_split[3].isdigit() and len(message_split) == 4: 
                logging.debug("BUY x FOR y")
                await message.channel.send(ruebotActions.buyrueb(author_id, message_split[1], message_split[3]))
                return
            elif message_split[0] == "buy" and len(message_split) > 4:
                await message.channel.send(msg_toomanyparam)
                return
            elif message_split[0] == "buy" and len(message_split) < 4:
                await message.channel.send(msg_missingparam)
                return
        except IndexError:
            pass
        
        #BUY END
        """
        
        
        #USER START
        try:
            if message_split[0] == "user":
                logging.debug("user")
                #USER REGISTER START
                try: 
                    if message_split[1] == "register" and len(message_split) == 2:
                        logging.debug("USER REGISTER")    
                        #Checks if user is registered and returns result as string
                        await message.channel.send(user.register(author_id, author_displayname))
                        logging.debug("USER REGISTER - FINISHED")
                        return
                    elif message_split[1] == "register":
                        logging.debug("USER REGISTER - too many parameters")
                        #Too many parameters
                        await message.channel.send(msg.tooManyParam(callbot+" user register"))
                        logging.debug("USER REGISTER - FINISHED")
                        return
                        
                except IndexError:
                    logging.debug("USER REGISTER - IndexError")
                    pass
                #USER REGISTER END
                
                
                #USER DELETE START
                try:
                    if message_split[1] == "delete" and len(message_split) == 2:
                        logging.debug("USER DELETE")
                        await message.channel.send(user.delete(author_id))
                        logging.debug("USER DELETE FINISHED")
                        return
                except IndexError:
                    logging.debug("USER DELETE - IndexError")
                    pass
                #USER DELETE END
                
   
                #USER ADDINFO START
                try:
                    if message_split[1] == "addinfo":
                        logging.debug("USER ADDINFO")
                        
                        #USER ADDINFO FRUIT START
                        try:
                            if message_split[2] == "fruit" and len(message_split) == 4:
                                logging.debug("USER ADDINFO FRUIT")
                                
                                #adds fruit to users 
                                await message.channel.send(addinfo.fruit(author_id, message_split[3]))
                                logging.debug("USER ADDINFO FRUIT - FINISHED")
                                return
                            elif message_split[2] == "fruit" and len(message_split) == 3:
                                #Parameter is missing
                                logging.debug("USER ADDINFO FRUIT - missing parameters")
                                await message.channel.send(msg.missingParam(callbot+" user addinfo fruit <fruit>"))
                                logging.debug("USER ADDINFO FRUIT - FINISHED")
                                return
                            
                            elif message_split[2] == "fruit" and len(message_split) > 4:
                                logging.info("USER ADDINFO FRUIT - too many parameters")
                                await message.channel.send(msg.tooManyParam(callbot+" user addinfo fruit <fruit>"))
                                logging.debug("USER ADDINFO FRUIT - FINISHED")
                                return
                            
                        except IndexError:
                            pass
                        #USER ADDINFO FRUIT END
                        
                        #USER ADDINFO FC START
                        try:
                            if message_split[2] == "fc" and len(message_split) == 4:
                                logging.debug("USER ADDINFO FC")
                                
                                #Fügt Friendcode dem Benutzereintrag in der db hinzu
                                await message.channel.send(addinfo.friendcode(author_id, message_split[3]))
                                logging.debug("USER ADDINFO FC - FINISHED")
                                return
                            elif message_split[2] == "fc" and len(message_split) == 3:
                                #Parameter is missing
                                logging.info("USER ADDINFO FC - missing parameters")
                                await message.channel.send(msg.missingParam(callbot+" user addinfo <friendcode>"))
                                logging.debug("USER ADDINFO FC - FINISHED")
                                return
                            
                            elif message_split[2] == "fc" and len(message_split) > 4:
                                logging.info("USER ADDINFO FC - too many parameters")
                                await message.channel.send(msg.tooManyParam(callbot+" user addinfo fc <friendcode>"))
                                logging.debug("USER ADDINFO FC - FINISHED")
                                return
                        except IndexError:
                            pass   
                        #USER ADDINFO FC END
                        
                        #USER ADDINFO PIRATE START
                        try:
                            if message_split[2] == "pirate" and len(message_split) == 4:
                                logging.debug("USER ADDINFO PIRATE")
                                #Fügt Friendcode dem Benutzereintrag in der db hinzu
                                await message.channel.send(addinfo.pirate(author_id, message_split[3]))
                                logging.debug("USER ADDINFO PIRATE - FINISHED")
                                return
                            elif message_split[2] == "pirate" and len(message_split) == 3:
                                #Parameter is missing
                                await message.channel.send(msg.missingParam(callbot+" addinfo pirate <true|false>"))
                                logging.debug("USER ADDINFO PIRATE - FINISHED")
                                return
                            
                            elif message_split[2] == "pirate" and len(message_split) > 4:
                                logging.info("USER ADDINFO PIRATE - too many parameters")
                                await message.channel.send(msg.tooManyParam(callbot+" addinfo pirate <true|false>"))
                                logging.debug("USER ADDINFO PIRATE - FINISHED")
                                return
                        except IndexError:
                            pass   
                        #USER ADDINFO PIRATE END
                except IndexError:
                    logging.debug("USER ADDINFO - IndexError")
                    pass
                #USER ADDINFO END
                
                
                #USER DELETEINFO START
                try:
                    if message_split[1] == "deleteinfo":
                        logging.debug("USER DELETEINFO")
                        
                        #USER DELETEINFO FC START
                        try:
                            if message_split[2] == "fc" and len(message_split) == 3:
                                logging.debug("USER DELETEINFO FC")
                                await message.channel.send(deleteinfo.friendcode(author_id))
                                logging.debug("USER DELETEINFO FC - FINISHED")
                                return
                            elif message_split[2] == "fc" and len(message_split) > 3:
                                #Too many parameters
                                logging.info("USER DELETEINFO FC - too many parameters")
                                await message.channel.send(msg.tooManyParam(callbot+" USER DELETEINFO FC"))
                                logging.debug("USER DELETEINFO FC - FINISHED")
                                return      
                        except IndexError:
                            pass
                        #USER DELETEINFO FC END
                except IndexError:
                    logging.debug("USER DELETEINFO - IndexError")
                    pass
                #USER DELETEINFO END
                
        except IndexError as e:
            logging.info("USER - IndexError: "+e)
            pass
        #USER END
        
        
        #PRICE START
        try:
            if message_split[0] == "price" and len(message_split) != 1:
                logging.debug("PRICE")
                #PRICE ADD START
                try:
                    if message_split[1] == "add" and len(message_split) == 3:
                        logging.debug("PRICE ADD")
                        await message.channel.send(price.add(message_split[2], author_id))  
                        logging.debug("PRICE ADD - FINISHED")                    
                        return
                
                    elif message_split[1] == "add" and len(message_split) == 2:
                        logging.info("PRICE ADD - Missing Parameter")
                        await message.channel.send(msg.missingParam(callbot+" price add <price>"))
                        logging.debug("PRICE ADD - FINISHED")   
                        return
                    elif message_split[1] == "add":
                        await message.channel.send(msg.tooManyParam(callbot+" price add <price>"))
                        logging.debug("PRICE ADD - FINISHED")
                        return
                except IndexError:
                    pass
                #PRICE ADD END
                
                
            #Missing parameters
            elif message_split[0] == "price":
                await message.channel.send(msg.missingParam(callbot+" price <param>"))
                logging.debug("PRICE - FINISHED")
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
                    if message_split[1] == "prices" and len(message_split) == 2 or message_split[1] == "price" and len(message_split) == 2:
                        logging.debug("LIST PRICES")
        
                        await message.channel.send(list.prices(author_id))
                        logging.debug("LIST PRICES - FINISHED")
                        return
                        
                    elif message_split[1] == "price" and len(message_split) > 2:
                        logging.debug("LIST PRICES - too many parameters")
                        await message.channel.send(msg.tooManyParam(callbot+" list prices"))
                        logging.debug("LIST PRICES - FINISHED")
                        return
                except IndexError:
                    pass
                #LIST PRICE END
                
                #LIST PRICEHISTORY START
                try:
                    #LIST PRICEHISTORY (no parameters)
                    if message_split[1] == "pricehistory" and len(message_split) == 2:
                        logging.debug("LIST PRICEHISTORY")
                        user_input = None
                        
                        #get pricehistory
                        await message.channel.send(list.pricehistory(author_id, user_input))
                        logging.debug("LIST PRICEHISTORY - FINISHED")
                        return
                    
                    #LIST PRICEHISTORY <USERNAME>
                    if message_split[1] == "pricehistory" and len(message_split) > 2:
                        logging.debug("LIST PRICEHISTORY <USERNAME>")
                        #print(message_split[2:])
                        await message.channel.send(list.pricehistory(author_id, message_split[2:]))
                        logging.debug("LIST PRICEHISTORY <USERNAME> - FINISHED")
                        return
                except IndexError:
                    pass
                #LIST PRICEHISTORY END
                
                #LIST USER <USERNAME> START
                try:
                    #LIST USER without username parameter
                    if message_split[1] == "user" and len(message_split) == 2:
                        logging.debug("LIST USER")
                        await message.channel.send(list.user(author_displayname))
                        logging.debug("LIST USER - FINISHED")
                        return
                    #LIST USER <USERNAME>
                    elif message_split[1] == "user" and len(message_split) >= 3:
                        logging.debug("LIST USER <USERNAME>")
                        await message.channel.send(list.user(message_split[2:]))
                        logging.debug("LIST USER <USERNAME> - FINISHED")
                        return
                except IndexError:
                    pass
                #LIST USER <USERNAME> END
                
        except IndexError:
            pass
        #LIST END
        
        #WENN NICHTS AUFGEFANGEN WURDE
        await message.channel.send('Ja da passt was mit dem Syntax nicht hmmm...')
        
        
    #Bot aufgerufen, ohne Parameter anzugeben
    elif message.content.lower() == callbot:
        logging.info("No Parameters after "+callbot)
        await message.channel.send("Ohne Parameter passiert hier nichts! '$RÜBot help' oder '$RÜBot help full' für eine Liste der Kommandos.")
    #$RÜBot ende   
           
    
try:
    client.run(ruebot.config.gettoken())
except Exception as e:
    print(e)
    sys.exit(0)
    