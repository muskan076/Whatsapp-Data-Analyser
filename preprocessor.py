import re
import pandas as pd

def pre(chat):
    chat = ' '.join(chat.split('\n'))

    dates = []
    pattern = re.compile(r'\d{2}/\d{2}/\d{2}\W\s\d{1,2}:\d{2}\s[a?|p?|m?]*')
    matches = pattern.finditer(chat)
    for match in matches:
        match = match.group()
        match = ''.join(match.split(','))
        dates.append(match)
    split = re.split(pattern, chat)[1:]

    df = pd.DataFrame({'date': dates, 'message': split})



    username = []
    user_message = []
    for message in df['message']:
        pattern = re.compile(r'-([\w\W]+?):\s')
        matches = re.split(pattern, message)
        if matches[1:]:
            username.append(matches[1])
            user_message.append(matches[2])
        else:
            username.append('notification')
            user_message.append(matches[0][2:])
    df['username'] = username
    df['user_message'] = user_message
    df.drop('message', axis=1, inplace=True)

    u = []
    for user in df['username']:
        space = user.strip()
        u.append(space)
    u_1 = []
    for mess in df['user_message']:
        space_1 = mess.strip()
        u_1.append(space_1)
    df['username'] = u
    df['user_message'] = u_1

    new = []
    if 'm' in df['date'][0]:
        for d in df['date']:
            if len(d) == 16:
                da = d[0:9] + '0' + d[9:]
                new.append(da)
            else:
                new.append(d)
        df['date'] = new
    else:
        pass

    dates = []
    if 'm' in df['date'][0]:
        for date in df['date']:
            if date[-2:] == 'am' and date[-8:-6] == '12':
                date = date[0:9] + '00' + date[-6:-3]
                dates.append(date)
            elif date[-2:] == 'am':
                date = date[:-2]
                dates.append(date)
            elif date[-2:] == 'pm' and date[-8:-6] == '12':
                date = date[:-2]
                dates.append(date)
            else:
                date = date[0:9] + str(int(date[9:11]) + 12) + date[-6:-3]
                dates.append(date)
        df['date'] = dates

    else:
        pass

    mm = []
    for m in df['date']:
        m = m.strip()
        mm.append(m)

    df['date'] = mm

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M')

    df['year'] = df['date'].dt.year

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day

    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    df['date_only'] = df['date'].dt.date

    df['day_name'] = df['date'].dt.day_name()


    ## creating a new column period for heatmap

    time = []
    for hour in df.hour:
        if hour == 23:
            time.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            time.append(str('00') + '-' + str(hour + 1))
        else:
            time.append(str(hour) + '-' + str(hour + 1))
    df['period'] = time


    return df






































