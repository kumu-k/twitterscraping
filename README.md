#twitter scraping

##using snscrape library and streamlit GUI

##mongoDB


*twitterscraping project scrape the data such as datae,id,url,tweet content,user,reply count,retweet count,language,source,count from twitter.

##instruction

*Copy paste code in PyCharm
*Run code in PyCharm terminal(eg:streamlit run ./twitter_scraping.py)
*It will open the streamlit GUI in a browser window.
*Input the scrapped  word,start date,end date,enter the number of tweet data and press the display data button.You can view the records in a table.
*If the desired word not available it shows "No data found " meassge.
*When you press save button records added to mongodb database and message displayed "Records successfully saved to DB".
*Select the download file type csv or json and press the download data button.File download in required format in download. 


*when you press save data button if you get DNS time out error.In Command promt run the followin code "ipconfig /flushdns" and  try to save file it will work.
