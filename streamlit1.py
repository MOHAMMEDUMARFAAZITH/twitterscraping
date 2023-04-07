#import libraries
import streamlit as st
import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
from PIL import Image
import graphviz
import snscrape
image = Image.open(r"C:\Users\RAZITH\Pictures\pic4.PNG")
st.image(image)

#st.header displays text in header formatting
st.header('TWITTER SCRAPING')
st.subheader("SCRAPE THE TWITTER DATA FROM TWITTER")


#st.selectbox displays a select widget
option = st.selectbox('WHAT WOULD YOU LIKE TO SEARCH?',('KEYWORD', 'HASHTAG'))
st.write('YOUR SELECTED:', option)


#st.text_input displays a single-line text input widget
scraped_word = st.text_input('PLEASE ENTER A '+option,("@elonmusk","#IPL23"))
st.write('THE SCRAPED WORD IS', scraped_word )


#st.date_input displays a date input widget
start_date = st.date_input("START_DATE",datetime.date(2023, 1, 1))
st.write('SELECT THE DATE RANGE FROM:', start_date)


#st.date_input displays a date input widget
end_date = st.date_input("END_DATE",datetime.date(2023, 1, 1))
st.write('SELECT THE DATE RANGE TO:', end_date)


#st.number_input displays a numeric input widget
tweet_count = st.number_input('INSERT A TWEET COUNT', min_value=10, max_value=10000, value=10, step=1)
st.write('THE NUMBER OF TWEET COUNT IS ', tweet_count)


#Created a list to append all tweet attributes(data)
attributes_container = []

query = f'{scraped_word} lang:en since:{start_date} until:{end_date}'

#Using TwitterSearchScraper to scrape data and append tweets to list
if (option=="KEYWORD") or (option=="HASHTAG"):
   for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
      if i>tweet_count-1:
         break
      attributes_container.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount,tweet.user.username])


#Creating a dataframe from the tweets list above 
col1, col2, col3, col4 = st.columns(4)
df = pd.DataFrame(
   attributes_container,
   columns=(["date", "id", "url", "tweet content","reply count", "retweet count","language", "source", "like count","username"]))
with col1:
   if st.button("SHOW DATA"):    
      st.write(df)
      st.success("SHOW DATAFRAME SUCCESSFULLY")


# using MongoClient to connect (mongodb+python)


client = pymongo.MongoClient("mongodb+srv://root:12345@cluster0.8pzyd4r.mongodb.net/test")
mydb = client["twitter_database"]
information = mydb.twitter_data


#upload dataframe into mongodb database
df["date"] = pd.to_datetime(df['date']).dt.date
df["date"] = pd.to_datetime(df['date'])  
a = df.to_dict("records")
date_range = f'since:{start_date} until:{end_date}'
b = {"Scraped_word":scraped_word,"Scraped_date_range":date_range,"Scraped_data":a}  
def upload_database(b):
   return b
call = upload_database(b)
with col2:
   e = st.button("UPLOAD TO DATABASE")  
if e:
   information.insert_one(call)
   st.success("UPLOAD THE DATA INTO MONGODB DATABASE SUCCESSFULLY")


#download dataframe as csv format
def download_csv(df):
   return df.to_csv(index=False).encode('utf-8')
with col3:
   csv = download_csv(df)
   c = st.download_button("DOWNLOAD DATA AS CSV FORMAT",csv,"file.csv","text/csv",key='download-csv')
if c:
   st.success("DOWNLOAD DATA AS CSV FORMAT SUCCESSFULLY")


#download dataframe as json format
def download_json(df):
   return df.to_json(orient="records")
with col4:
   json_string = download_json(df)
   d = st.download_button("DOWNLOAD DATA AS JSON FORMAT",json_string,"file.json","application/json",key='download-json')
if d:
   st.success("DOWNLOAD DATA AS JSON FORMAT SUCCESSFULLY")


# Create a graphlib graph object
with st.sidebar:
   graph = graphviz.Digraph()
   graph.edge('TWITTER SCRAPING', 'SELECT KEYWORD OR HASHTAG')
   graph.edge('SELECT KEYWORD OR HASHTAG', 'ENTER YOUR SCRAPED WORD')
   graph.edge('ENTER YOUR SCRAPED WORD', 'START DATE')
   graph.edge('START DATE', 'END DATE')
   graph.edge('END DATE', 'TWEET COUNT')
   graph.edge('TWEET COUNT', 'SHOW DATA')
   graph.edge('SHOW DATA', 'UPLOAD TO DATABASE')
   graph.edge('UPLOAD TO DATABASE', 'DOWNLOAD DATA AS CSV FORMAT')
   graph.edge('DOWNLOAD DATA AS CSV FORMAT', 'DOWNLOAD DATA AS JSON FORMAT')
   st.graphviz_chart(graph)