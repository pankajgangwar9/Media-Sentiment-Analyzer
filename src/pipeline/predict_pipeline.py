import os 
import sys
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject')
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject/src/')
from src.exception import CostumException
from src.logger import logging 
import pandas as pd

from src.components.data_ingestion import DataIngestion


class CustomData:
    def __init__(self, link: str):
        
        self.link = link

    def send_link(self):
        try:
            lnk=str(self.link)
            obj=DataIngestion(lnk)
            print(obj.initiate_data_ingestion())

        except Exception as e:
            raise CostumException(e,sys)