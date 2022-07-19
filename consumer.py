import json
from kafka import KafkaConsumer
import snowflake.connector
from send_data_to_DB import send_data_to_snowflake
from decouple import config

USER = config('USER')
PASSWORD = config('PASSWORD')
ACCOUNT = config('ACCOUNT')

print("Waiting on Messages ...")
if __name__ == '__main__':
    consumer = KafkaConsumer(
        'dbserver1.inventory.customers',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    con_def = snowflake.connector.connect(user=USER,
                                      password=PASSWORD, 
                                      account=ACCOUNT
                                     ) 
   
    db_cursor_def = con_def.cursor()
    database_connection = {"db_cursor_def":db_cursor_def}


    for message in consumer:

        consumer_data = json.loads(message.value)
        id = consumer_data['payload']['after']['id']
        first_name = consumer_data['payload']['after']['first_name']
        last_name = consumer_data['payload']['after']['last_name']
        email = consumer_data['payload']['after']['email']

        response = send_data_to_snowflake(database_connection, id, first_name, last_name, email )
        print(response)