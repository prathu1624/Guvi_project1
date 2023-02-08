#installing SNSCRAPE library
#pip install snscrape
#streamlit block
import streamlit as st
import datetime

  

#importing required modules
import pandas as pd
import snscrape.modules.twitter as sntwitter

#scraping the required data
def twitter_scrape(query,limit):
  scraper = sntwitter.TwitterSearchScraper(query)
  tweets=[]
  for i, tweet in enumerate(scraper.get_items()): #date, id, url, tweet content, user,reply count, retweet count,language, source, like count
    data = [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount
          ,tweet.retweetCount,tweet.lang, tweet.source,tweet.likeCount]
    tweets.append(data)
    if i == limit:
      break
  df = pd.DataFrame(tweets, columns=['date and time','id','content','user','reply','retweetcount','language','source','likecount'])
  df_sort = df.sort_values(by = 'date and time', ascending= False)
  return df_sort


  
def mongo_up(df):
#uploading dataframe to MongoDB
  from pymongo import MongoClient
  py = MongoClient("mongodb://guvi_prathu:prathu123@ac-xbyzunm-shard-00-00.i9y6wxn.mongodb.net:27017,ac-xbyzunm-shard-00-01.i9y6wxn.mongodb.net:27017,ac-xbyzunm-shard-00-02.i9y6wxn.mongodb.net:27017/?ssl=true&replicaSet=atlas-13sxpi-shard-0&authSource=admin&retryWrites=true&w=majority")
  p1 = py["Projects_GUVI"]
  project_collect = p1["Twitter_data"]
  project_collect.insert_many(df.to_dict('records'))
  
#streamlit
def streamlit():
  st.title("Twitter data scrapping")
  st.header("This is twitter scraper by Prathamesh.") 
  text = st.text_input("Text")
  htag = st.text_input("#Hashtag", placeholder = "Enter the hashtag", disabled = False, label_visibility='visible')
  uname = st.text_input("username", placeholder = "Enter the username", disabled = False, label_visibility='visible')
  startdt = st.date_input("Start date", datetime.date(2019,7,4))
  enddt = st.date_input("End date",datetime.date(2019,7,4))
  query = f"{text} (#{htag}) (from:{uname}) since:{startdt} until:{enddt}"
  limit=st.slider("No. of tweets", min_value=0, max_value=1000,label_visibility="visible")
  limit = int(limit)
  data = twitter_scrape(query,limit)
  st.dataframe(data=data)
  if st.button("Upload"):
     mongo_up(data)
  st.download_button("Download CSV", data = data.to_csv(), file_name="CSV_data")
  st.download_button("Download json", data = data.to_json(), file_name="json_data")  
    
maincall = streamlit()
