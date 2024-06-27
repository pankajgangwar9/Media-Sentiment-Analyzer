import os 
import sys
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject')
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject/src/')
from src.exception import CostumException
from src.logger import logging 
import pandas as pd
import csv

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
from urllib.request import Request
import logging
import ssl
from urllib.request import urlopen, Request
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass
    
    def read_csv(self):
        logging.info("Data Display for the end user->")
        try:
            def read_csv(filename):
                data = []
                with open(filename, 'r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        data.append(row)
                return data
        except Exception as e:
            raise CostumException(e,sys)