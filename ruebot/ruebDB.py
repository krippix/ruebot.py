import psycopg2
from ruebot import config
import logging



class ruebDatabaseError(Exception):
    pass


def dbrequest(sqlstatement, user_input):
    """ Connect to the PostgreSQL database server """
    #beispiel: dbconnect('SELECT id FROM users WHERE displayname=%s', 'krippix')
    
    conn = None
    try:
        # read connection parameters
        params = config.databaseconfig()
        
        # connect to the PostgreSQL server
        #logging.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute(sqlstatement, (user_input))
        
        #get one of the dbresults
        answer = cur.fetchone()
       
        # close the communication with the PostgreSQL
        cur.close()
        
        return answer
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        raise ruebDatabaseError(error)
    finally:
        if conn is not None:
            conn.close()
            #logging.debug('dbrequest: Database connection closed.')
 
def dbfetchall(sqlstatement, user_input):
    """ Connect to the PostgreSQL database server """
    #beispiel: dbconnect('SELECT id FROM users WHERE displayname=%s', 'krippix')
    
    conn = None
    try:
        
        # read connection parameters
        params = config.databaseconfig()
        
        # connect to the PostgreSQL server
        #logging.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute(sqlstatement, (user_input))

 
        # display the PostgreSQL database server version
        #print('PostgreSQL database version:')
        #cur.execute('SELECT version()')
        answer = cur.fetchall()
       
        # close the communication with the PostgreSQL
        cur.close()
        
        #print("-----ANSWER_START-----")
        #print(answer)
        #print("------ANSWER_END------")
        return answer
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        raise ruebDatabaseError(error)
    finally:
        if conn is not None:
            conn.close()
            #logging.debug('dbfetchall: Database connection closed.') 

def dbcommit(sqlstatement, user_input):
    """ Connect to the PostgreSQL database server """
    #beispiel: dbconnect('SELECT id FROM users WHERE displayname=%s', 'krippix')
    
    conn = None
    try:
        
        # read connection parameters
        params = config.databaseconfig()
        
        # connect to the PostgreSQL server
        #logging.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute(sqlstatement, (user_input))
        
        #Commit statement
        answer = conn.commit()
        
       
        # close the communication with the PostgreSQL
        cur.close()

        return answer
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        raise ruebDatabaseError(error)
    finally:
        if conn is not None:
            conn.close()
            #logging.debug('dbcommit: Database connection closed.')

