import streamlit as st
import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo

st.header('TWITTER SCRAPING')
st.subheader("Scrape the twitter data from twitter")

option = st.selectbox('What would you like to search?',('keyword', 'hashtag'))
st.write('You selected:', option)

scraped_word = st.text_input('Please enter a '+option,("@elonmusk","#IPL23"))
st.write('The scraped word is', scraped_word )

start_date = st.date_input("start_date",datetime.date(2022, 1, 1))
st.write('Select the date range from:', start_date)

end_date = st.date_input("end_date",datetime.date(2022, 1, 1))
st.write('Select the date range to:', end_date)

tweet_count = st.number_input('Insert a tweet count', min_value=1, max_value=10000, value=5, step=1)
st.write('The number of tweet count is ', tweet_count)

attributes_container = []
query = f'{scraped_word} lang:en since:{start_date} until:{end_date}'

if (option=="keyword") or (option=="hashtag"):
   for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
      if i>tweet_count:
         break
      attributes_container.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount,tweet.user.username])

df = pd.DataFrame(
   attributes_container,
   columns=(["date", "id", "url", "tweet content","reply count", "retweet count","language", "source", "like count","username"]))
if st.button("show data as pandas dataframe"):
   st.success("show dataframe Successfully")    
   st.write(df)

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = client["twitter_database"]
information = mydb.twitter_data
if st.button("upload dataframe into mongodb database"):
   st.success("upload data into mongodb database Successfully")   
   df["date"] = pd.to_datetime(df['date']).dt.date
   df["date"] = pd.to_datetime(df['date'])  
   a = tweets_df.groupby(['username',"date"]).apply(lambda x: x.to_dict(orient='records')).rename('scraped_data').reset_index().to_dict('records')
   information.insert_many(a)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Press to Download dataframe as csv format",csv,"file.csv","text/csv",key='download-csv')

json_string = df.to_json(orient="records")
st.download_button("Press to Download dataframe as json format",json_string,"file.json","application/json",key='download-json')