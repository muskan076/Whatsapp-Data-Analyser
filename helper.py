from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import re


def fetch_stats(selected_user,df1):

    if selected_user == 'Overall':
       over_all =  df1.shape[0]
       min_date = df1['date_only'].min()
       num_words = []
       for words in df1['user_message']:
           num_words.extend(words.split())
       media_count = len(df1[df1['user_message'] == '<Media omitted>'])

       urls = []
       extract = URLExtract()
       for messages in df1['user_message']:
           a = extract.find_urls(messages)
           urls.extend(a)
    else:
        user_df = df1[df1['username'] == selected_user]
        over_all = user_df.shape[0]
        min_date = user_df['date_only'].min()
        num_words = []
        for words in user_df['user_message']:
            num_words.extend(words.split())
        media_count = len(user_df[user_df['user_message'] == '<Media omitted>'])

        urls = []
        extract = URLExtract()
        for messages in user_df['user_message']:
            a = extract.find_urls(messages)
            urls.extend(a)

    return over_all,min_date,len(num_words),media_count, len(urls)

def most_busy_users(df1):
        a1 = df1['username'].value_counts().head()
        a2 = round((df1['username'].value_counts()/df1.shape[0]*100),2).head().reset_index().rename(
            columns={'index': 'username', 'username': 'Percent'})

        return a1,a2


def users_wordcloud(selected_user, df1):
    f = open('stopwords.txt', 'r')
    stopwords = f.read()



    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    def punctuations(message):
        res = ""
        for words in message:
            if words not in punc:
                res = res + words
        return res







    if selected_user == 'Overall':
        temp = df1[df1['user_message'] != '<Media omitted>']
        temp = temp[temp['username'] != 'notification']
        temp = temp[temp['user_message'] != 'This message was deleted']
        temp = temp[temp['user_message'] != 'You deleted this message']
        temp['user_message'] = temp['user_message'].apply(remove_stopwords)
        temp['user_message'] = temp['user_message'].apply(punctuations)




        wc = WordCloud(width = 500,height = 500,min_font_size = 10,
                       background_color = 'white')


        df_wc = wc.generate(temp['user_message'].str.cat(sep = ' '))
    else:
        user_df = df1[df1['username'] == selected_user]
        temp = user_df[user_df['user_message'] != '<Media omitted>']
        temp = temp[temp['username'] != 'notification']
        temp = temp[temp['user_message'] != 'This message was deleted']
        temp = temp[temp['user_message'] != 'You deleted this message']
        temp['user_message'] = temp['user_message'].apply(remove_stopwords)
        temp['user_message'] = temp['user_message'].apply(punctuations)

        wc = WordCloud(width = 500,height =300, min_font_size=10,background_color= 'white')


        df_wc = wc.generate(temp['user_message'].str.cat(sep = ' '))

    return df_wc

def most_used_words(selected_user, df1):
    f1 = open('stopwords.txt', 'r')
    stopwords = f1.read()

    def remove_stop(messageses):
        words = []
        for word in messageses.lower().split():
            if word not in stopwords:
                words.append(word)
        return " ".join(words)

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    def punctuations(me):
        res = ""
        for words in me:
            if words not in punc:
                res = res + words
        return res



    if selected_user == 'Overall':
        temp = df1[df1['username'] != 'notification']
        temp = temp[temp['user_message'] != '<Media omitted>']
        temp = temp[temp['user_message'] != 'This message was deleted']
        temp = temp[temp['user_message'] != 'You deleted this message']
        temp = temp.reset_index()
        temp['user_message'] = temp['user_message'].apply(remove_stop)
        temp['user_messages'] = temp['user_message'].apply(punctuations)

        listt = []
        for strings in temp['user_messages']:
            share = strings.split()
            listt.extend(share)
        top_10 = pd.DataFrame(Counter(listt).most_common(10))






    else:
        df1 = df1[df1['username'] == selected_user]
        temp = df1[df1['username'] != 'notification']
        temp = temp[temp['user_message'] != '<Media omitted>']
        temp = temp[temp['user_message'] != 'This message was deleted']
        temp = temp[temp['user_message'] != 'You deleted this message']
        temp = temp.reset_index()
        temp['user_message'] = temp['user_message'].apply(remove_stop)
        temp['user_messages'] = temp['user_message'].apply(punctuations)

        listt = []
        for strings in temp['user_messages']:
            share = strings.split()
            listt.extend(share)
        top_10 = pd.DataFrame(Counter(listt).most_common(10))
    return top_10


## for emoji(top 10)
def emoji_helper(selected_user,df1):
    if selected_user != 'Overall':
        df1 = df1[df1['username'] == selected_user]


    emojis_0 = []
    for usermessage in df1['user_message']:
        a = usermessage.split()
        emojis_0.extend(a)
    new_line_list = []
    list_table = []

    for word in emojis_0:
        emojis = emoji.distinct_emoji_list(word)
        new_line_list.extend([emoji.emojize(is_emoji) for is_emoji in emojis])
        list_table.extend([emoji.demojize(is_emoji) for is_emoji in emojis])

    emoji_df = pd.DataFrame(Counter(new_line_list).most_common(10))
    emoji_df.columns = ['Emoji', 'Counts']
    aa = Counter(list_table).most_common(10)
    new_col = []
    for i in aa:
        new_col.append(i[0])
    emoji_df['Description'] = new_col

    return emoji_df


def user_timeline(selected_user,df1):
    if selected_user != 'Overall':
        df1 = df1[df1['username'] == selected_user]
    timeline = df1.groupby(['year','month']).count()['user_message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['year'][i]) + '-' + timeline['month'][i])
    timeline['time'] = time
    return timeline

def daily_message(selected_user,df1):
    if selected_user != 'Overall':
        df1 = df1[df1['username'] == selected_user]
    daily_df = df1.groupby('date_only').count().reset_index()

    return daily_df

def message_count(selected_user,df1):
    if selected_user != 'Overall':
        df1 = df1[df1['username'] == selected_user]
    day_messages = df1['day_name'].value_counts()
    month_messages = df1['month'].value_counts()

    return day_messages, month_messages


def activity_heatmap(selected_user, df1):
    if selected_user != 'Overall':
        df1 = df1[df1['username'] == selected_user]
    pivot = df1.pivot_table(index='day_name', columns='period', values='user_message', aggfunc='count').fillna(0)

    return pivot




