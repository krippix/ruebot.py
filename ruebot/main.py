#python native
import logging
import sys
#part of project
import ruebot.config
from ruebot.actions import user
from ruebot.actions import list
from ruebot.actions import addinfo
from ruebot.actions import deleteinfo
from ruebot.actions import price
from ruebot import msg
from ruebot import getInfo
#external
from discord.ext import commands


#TODO: get botname from ini
#TODO: set version in config.py
#bot version
ruebot_version = "v.1.0.1"
#Bot displayname
ruebot_displayname = "$RÜBot"
#Variable for calling the bot
callbot = "$rübot "



#SET logginglevel
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)


#parameters for calling the bot
bot = commands.Bot(command_prefix=(callbot,'$RÜBot ','$Rübot '),case_insensitive=True)

#Removes default help command to allow custom one
bot.remove_command("help")



#message on succesful login
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))



#Check if userdata needs to be updated
@bot.event
async def on_message(message):
    
    #Exclude bot's msg
    if message.author == bot.user:
        return
    
    #Check if username was changed and do so in case it was
    if message.content.lower().startswith(callbot):
        if getInfo.userexists(message.author.id):
            logging.info("Checking if username was changed.")
            getInfo.updateDisplaynames(str(message.author), message.author.id)
    
    await bot.process_commands(message)
#END USERDATA UPDATE    



#Now the actual commands


###################################################################################################


#START GROUP: HELP
@bot.group(name="help", description="Returns all commands available")
async def _help(message):
    if message.invoked_subcommand is None:
        #TODO: (Maybe) make help dynamic
        #helptext = ">>> **"+ruebot_displayname+" "+ruebot_version+"**\n"
        #for command in bot.commands:
        #    helptext+=f"{command}\n"
        await message.send(msg.help_brief())
    return
#END HELP

#START HELP FULL
@_help.command(name="full",description="Gibt alle Kommandos aus.")
async def help_full(message):
    await message.send("Komplette Hilfe als direktnachricht gesendet!")
    await message.author.send(msg.help_full())
#END HELP FULL
#END GROUP: HELP

###################################################################################################

#START GROUP: USER
@bot.group(name="user")
async def _user(message):
    logging.debug("USER")
    if message.invoked_subcommand is None:
        print("wat")
        await message.send(msg.missingParam(callbot+"user <option>"))
        return
#END USER

#START USER REGISTER
@_user.command(name="register",description="Registriert den Benutzer in der Datenbank")
async def _user_register(message):
    logging.debug("USER REGISTER")     
    
    #Checks if user is registered and returns result as string
    await message.send(user.register(message.author.id, str(message.author)))
    logging.debug("USER REGISTER - FINISHED")
    return
#END USER REGISTER

#START USER DELTE
@_user.command(name="deregister",description="Löscht den Benutzer und alle Preise aus der Datenbank")
async def _delete(message):
    logging.debug("USER DELETE")
    await message.send(user.delete(message.author.id))
    logging.debug("USER DELETE FINISHED")
    return
#END USER DELETE

#########################################

#START GROUP: USER ADDINFO
@_user.group(name="addinfo",description="Fügt dem Benutzer informationen hinzu.")
async def _user_addinfo(message):
    logging.debug("USER ADDINFO")
    
    #check if any subcommands are submitted
    if message.invoked_subcommand is None: #_user_addinfo:
        await message.send(msg.missingParam(callbot+"user addinfo <param>"))
        return
#END USER ADDINFO

#START USER ADDINFO FRUIT <fruit>
@_user_addinfo.command(name="fruit",description="Fügt die native Frucht dem Profil hinzu.")
async def _user_addinfo_fruit(message, *args):
    logging.debug("USER ADDINFO FRUIT")
    
    #adds fruit to users 
    try:
        await message.channel.send(addinfo.fruit(message.author.id, str(args[0])))
        logging.debug("USER ADDINFO FRUIT - FINISHED")
        return
    except IndexError:
        await message.send(msg.missingParam("user addinfo fruit <fruit>"))
        logging.debug("USER ADDINFO FRUIT - FINISHED")
        return
#END USER ADDINFO FRUIT <fruit>

#START USER ADDINFO FC <friendcode>
@_user_addinfo.command(name="friendcode",description="Fügt den Freundescode des Nutzers hinzu. Format: SW-0000-0000-0000")
async def _user_addinfo_friendcode(message, *args):
    logging.debug("USER ADDINFO FRIENDCODE")
         
    #adds friendcode to the users data
    try:
        await message.channel.send(addinfo.friendcode(message.author.id, args[0]))
        logging.debug("USER ADDINFO FRIENDCODE - FINISHED")
        return
    except IndexError:
        await message.send(msg.missingParam("user addinfo friendcode <code>"))
        logging.debug("USER ADDINFO FRIENDCODE - FINISHED")
        return
#END USER ADDINFO FC <friendcode>

#START USER ADDINFO PIRATE <true|false>
@_user_addinfo.command(name="pirate",description="Notiert ob der Benutzer pirat/gebannt ist.")
async def _user_addinfo_pirate(message, *args):
    logging.debug("USER ADDINFO PIRATE")
         
    #adds friendcode to the users data
    try:
        await message.channel.send(addinfo.pirate(message.author.id, args[0]))
        logging.debug("USER ADDINFO PIRATE - FINISHED")
        return
    except IndexError:
        await message.send(msg.missingParam("user addinfo pirate <true|false>"))
        logging.debug("USER ADDINFO PIRATE - FINISHED")
        return
#END USER ADDINFO PIRATE <true|false>
#END GROUP: USER ADDINFO

#########################################

#START GROUP: DELETEINFO
@_user.group(name="deleteinfo",description="Löscht dem Benutzer hinzugefügte infos")
async def _user_deleteinfo(message):
    logging.debug("USER DELETEINFO")
    
    if message.invoked_subcommand is None:
        await message.send(msg.missingParam(callbot+"user deleteinfo <param>"))
        return
#END DELETEINFO

@_user_deleteinfo.command(name="friendcode",aliases=["fc"],description="Löscht den Freundescode des Benutzers")    
async def _user_deleteinfo_friendcode(message):
    logging.debug("USER DELETEINFO FRIENDCODE")
    
    await message.channel.send(deleteinfo.friendcode(message.author.id))
    logging.debug("USER DELETEINFO FC - FINISHED")
    return
#END USER DELETEINFO FRIENDCODE    
#END GROUP: DELETEINFO

#########################################

#END GROUP: USER


###################################################################################################


#START GROUP: LIST
@bot.group(name="list",description="")
async def _list(message):
    if message.invoked_subcommand is None:
        await message.send(msg.missingParam(callbot+"list <option>"))
    return
#END LIST

#START LIST PRICES
@_list.command(name=("prices"),aliases=["price"],description='Listet aktuelle Rübenpreise auf. (Priaten und "normale" Benutzer getrennt)')
async def _list_prices(message):
    logging.debug("LIST PRICES")
        
    await message.send(list.prices(message.author.id))
    logging.debug("LIST PRICES - FINISHED")
    return
#END LIST PRICES

#START LIST PRICEHISTORY
@_list.command(name="pricehistory",description="Listet die letzten Rübenpreise der aktuellen Woche auf. Freilassen für dich selbst.")
async def _list_pricehistory(message, *args):
    logging.debug("LIST PRICEHISTORY")
                        
    #without userinput and with input
    await message.channel.send(list.pricehistory(message.author.id, args))
    logging.debug("LIST PRICEHISTORY <USERNAME> - FINISHED")
    return                   
#END LIST PRICEHISTORY

#START LIST USER
@_list.command(name="user",description="Listet info eines Benutzers auf. Freilassen für selbst.")
async def _list_user(message, *args):
    logging.debug("LIST USER")
    
    if len(args) == 0:
        await message.channel.send(list.user(str(message.author.id)))
        logging.debug("LIST USER - FINISHED")
        return
    
    else:
        await message.channel.send(list.user(args))
    
    logging.debug("LIST USER - FINISHED")
    return
#END LIST USER
    
#END GROUP: LIST
    
###################################################################################################

#START GROUP: PRICE
@bot.group(name="price",description="")
async def _price(message):
    logging.debug("PRICE")
    
    if message.invoked_subcommand is None:
        return callbot+"price <option>"
#END PRICE

#START PRICE ADD
@_price.command(name="add",description="Schreibt den aktuellen Rübenpreis in die Datenbank (Zeitzone Europe/Berlin)")
async def _price_add(ctx, *args):
    logging.debug("PRICE ADD")
    
    if len(args) == 0:
        await ctx.send(msg.missingParam("price add <price>"))
        logging.debug("PRICE ADD - FINISHED")
        return
    
    elif len(args) > 1:
        await ctx.send(msg.tooManyParam("price add <price>"))
        logging.debug("PRICE ADD - FINISHED")
        return
        
    else:
        #bullshit
        if args[0] == "69":
            
            #emoji = discord.utils.get(discord.emojis, name=':regional_indicator_n:')
            #if emoji:
            emoji_tuple = ("🇳","🇮","🇨","🇪")
            
            for x in emoji_tuple:
                await ctx.message.add_reaction(x)
        #bullshit end
        
        await ctx.channel.send(price.add(args, ctx.author.id))  
        logging.debug("PRICE ADD - FINISHED")
        return   
#END PRICE ADD

#END GROUP: PRICE

###################################################################################################

#TODO: SELL, Profittracker. Rüben verfallen nach einer woche.
        
################################################################################################### 

#START Bot connection
try:
    bot.run(ruebot.config.gettoken())
except Exception as e:
    print(e)
    sys.exit(0)
#END Bot connection
    