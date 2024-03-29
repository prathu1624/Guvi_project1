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
  py = MongoClient(#Enter your own MongoDB link)
  p1 = py["Projects_GUVI"]
  project_collect = p1["Twitter_data"]
  project_collect.insert_many(df.to_dict('records'))
  
#streamlit
def streamlit():
  
  st.title(":blue[Twitter Scrapping]")
  st.header(":violet[Welcome to twitter scrapper by Prathamesh.]") 
  text = st.text_input("Search Query", placeholder = "Enter your query")
  uname = st.text_input("username", placeholder = "Enter the username", disabled = False, label_visibility='visible')
  startdt = st.date_input("Start date", datetime.date(2023,1,4))
  enddt = st.date_input("End date",datetime.date(2023,1,4))
  query = f"{text} (from:{uname}) since:{startdt} until:{enddt}"
  limit=st.number_input("No. of tweets", min_value=0, max_value=1000,label_visibility="visible")
  limit = int(limit)
  data = twitter_scrape(query,limit)
  st.balloons()
  st.dataframe(data=data)
  if st.button("Upload"):
     mongo_up(data)
  st.download_button("Download CSV", data = data.to_csv(), file_name="CSV_data")
  st.download_button("Download json", data = data.to_json(), file_name="json_data")  
    
maincall = streamlit()
