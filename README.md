# $RÜBot Discord Bot

A Discord bot for tracking Animal Crossing turnip prices of multiple users.


# Requirements
discord.py
https://github.com/Rapptz/discord.py

texttable 
https://pypi.org/project/texttable/

psycopg2
https://pypi.org/project/psycopg2/

The file default-config.ini should be copied to config.ini in order to be regognized.


# Commands (german):
```
$RÜBot
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

Für Feedback oder informationen bezüglich des Bots bin ich per Mail oder auf Discord erreichbar: krippix#8372 | ruebot@gustelgang.de
Fragt mich nicht warum die Commands englisch sind, ich weiß es doch auch nicht :(

# Database behind ruebot
![Image of Database](https://raw.githubusercontent.com/krippix/ruebot.py/master/database.PNG)



