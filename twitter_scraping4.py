import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import json
import pymongo
import os

#get the data from interface
def get_data(search_word, start_date, end_date, tweet_count):
    scraped_data = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{search_word} since:{start_date} until:{end_date}").get_items()):
        if i >= tweet_count:
            break
        scraped_data.append({
            "date": tweet.date.strftime("%Y-%m-%d %H:%M:%S"), # Convert date to string
            "id": tweet.id,
            "url": tweet.url,
            "tweet_content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        })
    return scraped_data

#save
def save_to_mongodb(scraped_data):
    client = pymongo.MongoClient(
        "mongodb+srv://kk:123@cluster0.le0owl3.mongodb.net/test?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
    db = client.twitter
    scraped = db.scraped
    scraped.insert_many(scraped_data)

import os
#download
def download_data(scraped_data, file_format):
    if file_format == "json":
        with open("data.json", "w") as f:
            json.dump(scraped_data, f)
        # Save file to user's downloads folder
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", "data.json")
        with open(file_path, "w") as f:
            json.dump(scraped_data, f)
    elif file_format == "csv":
        df = pd.DataFrame(scraped_data)
        df.to_csv("data.csv", index=False)
        # Save file to user's downloads folder
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", "data.csv")
        df.to_csv(file_path, index=False)


# Create GUI
search_word = st.text_input("Scrapped word")
start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
end_date = st.date_input("End date", datetime.now())
tweet_count = st.number_input("Enter number of scrapped data", min_value=1, value=100)
file_format = st.selectbox("Select file format", ["json", "csv"])
display_button = st.button("Display data")
save_button = st.button("Save data")
download_button = st.button("Download data")

#when press button following code excutes
if display_button:
    scraped_data = get_data(search_word, start_date, end_date, tweet_count)
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        st.dataframe(df)
    else:
        st.write("No data found.")
if save_button:
    scraped_data = get_data(search_word, start_date, end_date, tweet_count)
    save_to_mongodb(scraped_data)
    st.write("Records successfully saved to DB")
if download_button:
    scraped_data = get_data(search_word, start_date, end_date, tweet_count)
    download_data(scraped_data, file_format)
    st.write("Record Downloaded successfully ")