# create table
sql_table_creation_commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id integer PRIMARY KEY,
            firstName varchar(255),
            lastName varchar(255),
            address varchar(255),
            city varchar(255),
            country varchar(255),
            zipCode varchar(10),
            email varchar(255),
            birthDate timestamp, 
            gender varchar(50),
            isSmoking BOOLEAN, 
            profession varchar(255),
            income  NUMERIC,
            createdAt timestamp,
            updatedAt timestamp 
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS subscription(
            id SERIAL PRIMARY KEY,
            user_id integer,
            subscription_createdAt timestamp,
            subscription_startDatet timestamp,
            subscription_endDate timestamp,
            subscription_status varchar(50),
            subscription_amount NUMERIC,
            CONSTRAINT fk_customer FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS messages (
            id integer PRIMARY KEY,
            senderId integer, 
            receiverId integer, 
            message varchar(255),
            createdAt timestamp
        )
        """
]

# insert query
sql_insert_user = """INSERT INTO users (user_id,firstName,lastName,address,city,country,zipCode,email,birthDate,gender,isSmoking,profession,income,createdAt,updatedAt)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TO_TIMESTAMP(%s,'YYYY/MM/DD'), %s, %s, %s,%s,TO_TIMESTAMP(%s,'YYYY/MM/DD'), TO_TIMESTAMP(%s,'YYYY/MM/DD'))"""
sql_insert_subscription = """ INSERT INTO subscription (user_id ,subscription_createdAt,subscription_startDatet,subscription_endDate,subscription_status,subscription_amount)
                                                VALUES ( %s,TO_TIMESTAMP(%s,'YYYY/MM/DD'), TO_TIMESTAMP(%s,'YYYY/MM/DD'), TO_TIMESTAMP(%s,'YYYY/MM/DD'), %s, %s)"""
sql_insert_message = """ INSERT INTO messages (id,senderId,receiverId,message,createdAt)
                                                        VALUES ( %s,%s, %s,%s, TO_TIMESTAMP(%s,'YYYY/MM/DD'))"""

# select query
total_messages_per_day = 'select to_char(createdAt,\'DD-MM-YYYY\') as day, count(*) as total from messages group by createdAt'
user_did_not_receive_any_message = 'select user_id ,city, country, email, to_char(createdAt,\'DD-MM-YYYY\') as created_date, to_char(updatedAt,\'DD-MM-YYYY\') as updated_date from users where user_id not in (select distinct receiverId from messages )'
total_subs_today = 'Select to_char(CURRENT_DATE,\'DD-MM-YYYY\') as to_day , count(id) as total_active_subscriptions from subscription where subscription_startDatet =(SELECT CURRENT_DATE) and subscription_status =\'Active\' '
sender_without_active_sub = 'select distinct user_id ,city, country, email, to_char(createdAt,\'DD-MM-YYYY\') as created_date, to_char(updatedAt,\'DD-MM-YYYY\') as updated_date from users u where user_id not in (select user_id from subscription where subscription_status = \'Active\') and user_id in (select senderId from messages)'
average_subscription_per_year_month ='select to_char(subscription_createdAt,\'YYYY-MM\') as year_month, (sum(subscription_amount)/count(distinct id)) as avreage from subscription group by 1 '