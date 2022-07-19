import logging # Used to display messages instead of just printing them
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from decouple import config

ROLE_ACCOUNT = config('ROLE_ACCOUNT')
WAREHOUSE = config('WAREHOUSE')
DATABASE = config('DATABASE')

def send_data_to_snowflake(database_connection, id, first_name, last_name, email):

    try:
        database_connection["db_cursor_def"].execute(f"USE ROLE {ROLE_ACCOUNT}")
        database_connection["db_cursor_def"].execute(f"USE WAREHOUSE {WAREHOUSE}")
        database_connection["db_cursor_def"].execute(f"USE DATABASE {DATABASE}")
    
        database_connection["db_cursor_def"].execute(
            "INSERT INTO customers (id, first_name, last_name, email ) "
            "VALUES(%s, %s, %s, %s)", (
                id, 
                first_name,
                last_name, 
                email
            ))
    except:
        pass

    logging.info('Total rows inserted: %s', database_connection["db_cursor_def"].rowcount)
    database_connection["db_cursor_def"].close()
    return "Done Sending"