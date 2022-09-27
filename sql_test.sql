# total_messages_per_day
select to_char(createdAt,'DD-MM-YYYY') as day, count(*) as total
from messages group by createdAt;

# user_did_not_receive_any_message
select user_id ,city, country, email, to_char(createdAt,'DD-MM-YYYY') as created_date, to_char(updatedAt,'DD-MM-YYYY') as updated_date
from users
where user_id not in (select distinct receiverId from messages);

# total_subs_today
select to_char(CURRENT_DATE,'DD-MM-YYYY') as to_day , count(id) as total_active_subscriptions
from subscription
where subscription_startDatet =(SELECT CURRENT_DATE)
  and subscription_status ='Active';

# sender_without_active_sub
select distinct user_id ,city, country, email, to_char(createdAt,'DD-MM-YYYY') as created_date, to_char(updatedAt,'DD-MM-YYYY') as updated_date
from users u
where user_id not in (select user_id from subscription where subscription_status = 'Active')
  and user_id in (select senderId from messages);

# average_subscription_per_year_month
select to_char(subscription_createdAt,'YYYY-MM') as year_month, (sum(subscription_amount)/count(distinct id)) as avreage
from subscription group by 1 ;