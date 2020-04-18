# $RÜBot Discord Bot

A Discord bot for tracking Animal Crossing turnip prices of multiple users.


### Database behind ruebot
![Image of Database](https://raw.githubusercontent.com/krippix/ruebot.py/master/database.PNG)


The file default-config.ini should be copied to config.ini in order to be regognized.


### Help Text (german):

$RÜBot v.1.0.0

    help                                Gibt kurze Hilfe aus
    help full                           Sendet gesamte hilfe als DM

    list price                          Listet alle aktuellen Rübenpreise auf
    list pricehistory <username>        Listet die letzten Rübenpreise der aktuellen Woche auf. Freilassen für selbst.
    list user <username>                Listet info eines Benutzers auf. Freilassen für selbst.
                      
    price add <price>                   Schreibt den aktuellen Rübenpreis in die Datenbank (Zeitzone Europe/Berlin)
    
    buy <quantity> at <price> (TODO)   Notiert den kauf von x Rüben für y Sternis
    sell <quantity> at <price> (TODO)  Notiert den verkauf von x Rüben für y Sternis

Sofern kein Benutzername angegeben werden kann gilt das command für den ausführenden!

    user register                       Registriert den Benutzer in der $RÜBot Datenbank.
    user delete                         Löscht den Benutzer unwiderruflich aus der Datenbank.
    
    user addinfo fruit <fruit>          Fügt die native Frucht dem Profil hinzu. (pear, cherry, orange, apple, peach)
    user addinfo pirate <param>         Pirat (arr) <true|false>
    user addinfo fc <friendcode>        Fügt den Freundescode des Nutzers hinzu. Format: SW-0000-0000-0000
    
    user deleteinfo fc                  Löscht den Freundescode des betreffenden Benutzers
    

Für Feedback oder informationen bezüglich des Bots bin ich per Mail oder auf Discord erreichbar: krippix#8372 | ruebot@gustelgang.de
Fragt mich nicht warum die Commands englisch sind, ich weiß es doch auch nicht :(


