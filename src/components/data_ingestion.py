import os 
import sys
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject')
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject/src/')
from src.exception import CostumException
from src.logger import logging 
import pandas as pd

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
from urllib.request import Request
import logging
import ssl
from urllib.request import urlopen, Request
from src.components.model_trainer import ModelTrainer
from bs4 import BeautifulSoup

from itertools import islice
from youtube_comment_downloader import *

class DataIngestion:
    def __init__(self,data_link):
        self.ingestion_config=data_link
    
    def initiate_data_ingestion(self):
        logging.info("Enter the data ingestion method or component.->")
        try:
            link=self.ingestion_config
            res=[]
            imdb="imdb"
            flipkart="flipkart"
            youtube="youtube"
            if link.count(imdb,0,len(link)):
                # Create a custom SSL context that doesn't verify the certificate
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                # Make the request using the custom SSL context
                request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(request, context=ssl_context)

                # Read and print the response
                data = response.read()
                imdb_html=bs(data,'html.parser')
                big_box=imdb_html.findAll('div',{"class":"redesign","id":"content-2-wide"})

                for box in big_box:
                    # Now you can apply find_all on each box
                    imdb_lister = box.find_all('div', {"class": "lister"})
                
                imdb_lister_list= box.find_all('div', {"class": "lister-list"})
                imdb_lister_list= box.div.find_all('div', {"class": "lister-item-content"})
                n=len(imdb_lister_list)

                for i in range(n):
                    prac=imdb_lister_list[i].find_all('div', {"class": "text show-more__control"})
                    res.append(prac)


            elif link.count(flipkart,0,len(link)):
                
                # User-Agent and Accept-Language headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'Accept-Language': 'en-us,en;q=0.5'
                }
                # Loop through the pages to collect comments
                for i in range(1, 4):  # Assuming you're scraping through 3 pages
                    # Construct the URL for the current page
                    page_url = f"{link}&page={i}"

                    # Send a GET request to the page
                    response = requests.get(page_url, headers=headers)

                    # Check if the request was successful
                    if response.status_code == 200:
                        # Parse the HTML content
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Extract comments using correct class name
                        cmt = soup.find_all('div', class_='ZmyHeo')  # Update if needed
                        for c in cmt:
                            # Get the comment text
                            comment_text = c.div.div.get_text(strip=True)
                            res.append(comment_text)

            elif link.count(youtube,0,len(link)):
                downloader = YoutubeCommentDownloader()
                comments = downloader.get_comments_from_url(link, sort_by=SORT_BY_POPULAR)
                for comment in islice(comments, 30):
                    res.append(comment['text'])
            



            modeltrainer=ModelTrainer(res)
            modeltrainer.model_predict()
        except Exception as e:
            raise CostumException(e,sys)
        


if __name__=="__main__":
    lnk=str(input("Enter link: "))
    obj=DataIngestion(lnk)
    print(obj.initiate_data_ingestion())