import configparser
import sys

#name of inifile
inifile = 'config.ini'

 
def checkini(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    
    return True #True = it works

def databaseconfig(filename='config.ini', section='postgresql'):
    # create a parser
    parser = configparser.ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db
#END DATABASECONFIG

def gettoken():
    #Retrieve token from ini
    
    #name of section for token
    section = 'botconfig'
    tokenname = 'token'
    
    #get token for login from ini
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