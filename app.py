import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat = bytes_data.decode('utf-8')
    df1 = preprocessor.pre(chat)

    # now we have a data frame of our chat by using above
    # fetch the username for our drop down
    user_list = df1['username'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Choose analysis acc to: ', user_list)

    if st.sidebar.button('Show Analysis'):

        stat_messages = helper.fetch_stats(selected_user,df1)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.subheader('Total messages')
            st.title(stat_messages[0])
        with col2:
            st.subheader('Links Shared')
            st.title(stat_messages[4])
        with col3:
            st.subheader('Total words')
            st.title(stat_messages[2])
        with col4:
            st.subheader('Total media Shared')
            st.title(stat_messages[3])
        with col5:
            st.subheader('Start date')
            st.title(stat_messages[1])
        if selected_user == 'Overall':
            users, table = helper.most_busy_users(df1)
            st.title('Most busy Users')
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(users.index, users.values,color = ['#8B3626', '#CD4F39', '#CD7054', '#EE8262', '#FF8C69'])
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(table)
        ## timeline of a user
        st.title('Monthly messages Timeline')
        timeline = helper.user_timeline(selected_user,df1)
        fig, ax = plt.subplots()
        ax.plot(timeline.time,timeline.user_message,color = '#EE0000')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # daily timeline

        st.title('Daily Timeline')
        daily_df = helper.daily_message(selected_user,df1)
        fig, ax = plt.subplots()
        ax.plot(daily_df['date_only'],daily_df['user_message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # day and month messages count

        col1, col2 = st.columns(2)
        day_wise, month_wise  = helper.message_count(selected_user, df1)
        with col1:
            st.header('Most Busy Days')
            fig, ax = plt.subplots()
            ax.bar(day_wise.index, day_wise.values,color = '#CD5555')
            plt.xticks(rotation = 'vertical',fontsize = 13)
            st.pyplot(fig)
        with col2:
            st.header('Most busy Months')
            fig, ax = plt.subplots()
            ax.barh(month_wise.index, month_wise.values,color = '#CD5C5C')
            plt.xticks(rotation='vertical',fontsize = 13)
            plt.yticks(fontsize = 15)

            st.pyplot(fig)







        ## wordcloud
        st.title('WordCloud')
        word = helper.users_wordcloud(selected_user,df1)
        fig,ax = plt.subplots()
        ax.imshow(word)
        st.pyplot(fig)

        ## for most common words
        st.title('Most Common words')
        words_return =  helper.most_used_words(selected_user,df1)


        fig, ax = plt.subplots()

        ax.bar(words_return[0],words_return[1], color ='#87CEFA')
        plt.xticks(rotation = 'vertical')

        st.pyplot(fig)

        # for emojis display

        st.title('Most Used Emojis')

        col1, col2 = st.columns(2)
        emoji_df = helper.emoji_helper(selected_user, df1)

        with col1:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Counts'].head(),labels = emoji_df['Emoji'].head(),autopct = '%.2f')

            st.pyplot(fig)
        with col2:
            st.dataframe(emoji_df)

        st.title('Weekly Actitvity Heatmap based on hours')
        heatmap = helper.activity_heatmap(selected_user, df1)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)




