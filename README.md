# Change Data Capture of Postgres to Snowflake using Debezium and Kafka Connect

* Clone the repository using the command below. 
```bash
git clone https://github.com/DevilIsdefeated/postgres-snowflake-debezium.git
```

* Specify the debezium version.
```bash
export DEBEZIUM_VERSION=1.9
```

* Start the Postgres Connector
```bash
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @postgres-connection-credential.json
```

* Consume messages from a Debezium topic
```bash
docker-compose -f docker-compose-postgres.yaml exec kafka /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --property print.key=true \
    --topic dbserver1.inventory.customers
```


* Modify the records in the database via Postgres client. 
```bash
docker-compose -f docker-compose-postgres.yaml exec postgres env PGOPTIONS="--search_path=inventory" bash -c 'psql -U $POSTGRES_USER postgres'
```

* See the records in the customers table.
```bash
SELECT * FROM customers;
```

* Insert into the customers table
```bash
INSERT INTO customers (id, first_name, last_name, email) VALUES (1, 'Bob', 'Frank', 'XXXXXXXXXXXXXXXX@gmail.com');
```
You should now see that the new data is been published into the consumer terminal. 

* Specify your Snowflake database credentials. I have included a sample environment variables. 
```bash
USER=XXXXXXXX
PASSWORD=XXXXXXXXX
ACCOUNT=XXXXXXXX.eu-central-1
ROLE_ACCOUNT=XXXXXXXXXXXX
WAREHOUSE=COMPUTE_WH
DATABASE=INVENTORY
```
* Install the necessary libraries. 
```bash
pip install -r requirements.txt
```


* Open another terminal and start the Python consumer script to get and process the data for your downstream application
```bash
python consumer.py
```

* Update a row in your customers table.
```bash
UPDATE customers
SET email = 'newemail@test.com'
WHERE id = 1004;
```

* Go to your Postgres databases and insert into the customers table. 
```bash
INSERT INTO customers(id, first_name, last_name, email) VALUES (1100, 'Tiana', 'West', 'Tiana.West@test.com');
```


* Some helpful snowflake SQL query to help with your implementation
```bash
-- use role sysadmin;
-- CREATE DATABASE inventory;
-- CREATE TABLE inventory."PUBLIC".customers (id int, first_name string, last_name string, email string);
-- SHOW DATABASES;
-- USE INVENTORY;
-- DESC TABLE customers;
-- INSERT INTO customers(id, first_name, last_name, email) VALUES (1100, 'Tiana', 'West', 'Tiana.West@test.com');
-- SELECT * from customers;
-- truncate table if exists customers; # DELETES ALL ROWS IN SNOWFLAKE TABLE
```
