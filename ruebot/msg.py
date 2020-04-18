#project internal
from ruebot import config


def NotReg():
    return "Du musst dich registrieren um diesen Befehl nutzen zu können: '$RÜBot user register'"


def DbError():
    return "Fehler bei der Datenbankverbindung - Versuche es später nochmal."

def tooManyParam(syntax):
    
    return "Zu viele Parameter. Syntax: '"+syntax+"'"
#END toomanyparam


def missingParam(syntax):
    return "Fehlende(r) Parameter. Syntax: '"+syntax+"'"
#END missingParam()


def noUser():
    return "Fehler - Kein Benutzer gefunden!"

def about():
    return """
>>> **"""+config.bot_name()+" "+config.bot_version()+"""**

Für Feedback oder informationen bezüglich des Bots bin ich per Mail oder auf Discord erreichbar: krippix#8372 | ruebot@gustelgang.de

https://github.com/krippix/ruebot.py
"""
    
def help_full():
    return """
```
**"""+config.bot_name()+" "+config.bot_version()+"""**

    help                                Gibt kurze Hilfe aus
    help full                           Sendet gesamte hilfe als DM
    
    about                               Gibt zusätzliche informationen zum Bot aus

    list price                          Listet alle aktuellen Rübenpreise auf
    list pricehistory <username>        Listet die letzten Rübenpreise der aktuellen Woche auf. Freilassen für selbst.
    list user <username>                Listet info eines Benutzers auf. Freilassen für selbst.
                      
    price add <price>                   Schreibt den aktuellen Rübenpreis in die Datenbank (Zeitzone Europe/Berlin)
    
    buy <quantity> at <price> (TODO)    Notiert den kauf von x Rüben für y Sternis
    sell <quantity> at <price> (TODO)   Notiert den verkauf von x Rüben für y Sternis

    user register                       Registriert den Benutzer in der $RÜBot Datenbank.
    user deregister                     Löscht den Benutzer und alle Preise aus der Datenbank
    
    user addinfo fruit <fruit>          Fügt die native Frucht dem Profil hinzu. (pear, cherry, orange, apple, peach)
    user addinfo pirate <true|false>    Notiert ob der Benutzer pirat/gebannt ist.
    user addinfo friendcode <code>      Fügt den Freundescode des Nutzers hinzu. Format: SW-0000-0000-0000
    
    user deleteinfo friendcode          Löscht den Freundescode des betreffenden Benutzers
```
"""

def help_brief():
    return """
>>> **"""+config.bot_name()+" "+config.bot_version()+"""**

help
help full

about

list price
list pricehistory <username>
list user <username>
                      
price add <price>

buy <quantity> at <price> (TODO)
sell <quantity> at <price> (TODO)

user register
user deregister                  
    
user addinfo fruit <fruit>          
user addinfo pirate <true>/<false>
user addinfo fc <friendcode>

user deleteinfo fc

"""