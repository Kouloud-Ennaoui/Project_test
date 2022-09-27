## Data sources

- the bellow two end point represent our data which it will be consumed , processed and loaded in tables in postgres database 

- [https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/users] -  contain data about users and the associated subscription to them
- [https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/messages](./courses.json) - contain data about the messages 

## Files description 
- ***requirements.txt*** : Contain modules that we need to install 
- ***database.ini***: A Configuration file that hold information about the database connection (this should not be loaded in git but you need those information to establish the connection with the database)
- ***config.py***: a configuration file to establish the connection with the database 
- ***dataprocesser.py***: Contain function to consume the data and to process it 
- ***sqlquery.py***: Contain all the queries (create tables queries, insert into tables queries and select queries) 
- ***sql_test.sql***: Contain SQL queries to meet the PO requirements
- ***Main.py*** : the main script (our entrypoint)

- ***Data warehouse schema.pdf***: The answer of question number 2 

##  Run  instructions: 
- You need to install PostgreSQL:
- In the cmd/terminal: 
  ```
  pip install -r requirements.txt
  ```
 