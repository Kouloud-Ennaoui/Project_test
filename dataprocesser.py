import json
import requests
import pandas as pd
from itertools import chain


def data_reader(url):
    response_api = requests.get(url)
    data = response_api.text
    # parse_json = json.loads(data)
    return json.loads(data)


def user_data_parser():
    parse_json = data_reader('https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/users')
    # parse data in dataframe
    df_user = pd.DataFrame(parse_json, columns=['createdAt', 'updatedAt', 'firstName', 'lastName', 'address', 'city',
                                                'country', 'zipCode', 'email', 'birthDate', 'profile', 'subscription',
                                                'id'])
    df_user = pd.concat([df_user.drop(['profile'], axis=1), df_user['profile'].apply(pd.Series)], axis=1)

    # get the subscription data and associate it with the user id
    list_user_sub = [{'user_id': r['id'], 'sub': r['subscription']} for i, r in df_user.iterrows()]
    list_subscription = list(
        chain(*[[{'user_id': item['user_id'], **s} for s in item['sub']] for item in list_user_sub]))
    df_sub = pd.DataFrame(list_subscription)
    # change data type
    df_sub['user_id'] = df_sub['user_id'].apply(pd.to_numeric)
    df_sub['amount'] = df_sub['amount'].apply(pd.to_numeric)

    # order the columns
    df_user = df_user[
        ['id', 'firstName', 'lastName', 'address', 'city', 'country', 'zipCode', 'email', 'birthDate', 'gender',
         'isSmoking', 'profession', 'income', 'createdAt', 'updatedAt']]

    # change data type
    df_user['id'] = df_user['id'].apply(pd.to_numeric)
    df_user['income'] = df_user['income'].apply(pd.to_numeric)
    return df_user, df_sub


def message_data_parser():
    parse_json = data_reader('https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/messages')
    df_msg = pd.DataFrame(parse_json, columns=["id", "senderId", "receiverId", "message", "createdAt"])
    df_msg['id'] = df_msg['id'].apply(pd.to_numeric)
    df_msg['senderId'] = df_msg['senderId'].apply(pd.to_numeric)
    df_msg['receiverId'] = df_msg['receiverId'].apply(pd.to_numeric)
    return df_msg

