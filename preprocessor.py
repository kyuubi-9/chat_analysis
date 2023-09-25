import re
import pandas as pd

def preprocess(data):
    split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
            '12hr' : '%d/%m/%Y, %I:%M %p - ',
            '24hr' : '%d/%m/%Y, %H:%M - ',
            'custom': ''
        }

    key = '12hr'

    user_msg = re.split(split_formats[key], data) [1:]
    date_time = re.findall(split_formats[key], data)
    df = pd.DataFrame({'date_time': date_time, 'user_msg': user_msg})

    df['date_time'] = pd.to_datetime(df['date_time'], format=datetime_formats[key])
    df.rename(columns={'date_time': 'date'}, inplace=True)


    usernames = []
    msgs = []
    for i in df['user_msg']:
            a = re.split('([\w\W]+?):\s', i) # lazy pattern match to first {user_name}: pattern and spliting it aka each msg from a user
            if(a[1:]): # user typed messages
                usernames.append(a[1])
                msgs.append(a[2])
            else: # other notifications in the group(eg: someone was added, some left ...)
                usernames.append("group_notification")
                msgs.append(a[0])

        # creating new columns
    df['user'] = usernames
    df['message'] = msgs

        # dropping the old user_msg col.
    df.drop('user_msg', axis=1, inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
