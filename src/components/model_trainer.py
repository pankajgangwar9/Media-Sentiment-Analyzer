import os 
import sys
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject')
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject/src/')
from src.exception import CostumException 
from src.logger import logging

import csv
import pandas as pd
import numpy as np
import src.components.text_normalizer as tn
from tensorflow.keras.preprocessing.sequence import pad_sequences
np.set_printoptions(precision=2, linewidth=80)


class ModelTrainer:
    def __init__(self,comm) -> None:
        self.comm=comm

    def model_predict(self):
        logging.info("Split Training and Test input data")
        try:
            import pickle
            model_path = 'E:/FinalYearProject/FinalYearProject/artifacts/model.pkl'
            with open(model_path,'rb') as file:
                trained_model=pickle.load(file)


            test_path = 'E:/FinalYearProject/FinalYearProject/artifacts/test_reviews.pkl'
            with open(test_path,'rb') as file:
                norm_test_reviews=pickle.load(file)


            train_path = 'E:/FinalYearProject/FinalYearProject/artifacts/train_reviews.pkl'
            with open(train_path,'rb') as file:
                norm_train_reviews=pickle.load(file)


            tokenized_train = [tn.tokenizer.tokenize(text) for text in norm_train_reviews]
            tokenized_test = [tn.tokenizer.tokenize(text) for text in norm_test_reviews]


            from collections import Counter
            # build word to index vocabulary
            token_counter = Counter([token for review in tokenized_train for token in review])
            vocab_map = {item[0]: index+1 for index, item in enumerate(dict(token_counter).items())}
            max_index = np.max(list(vocab_map.values()))
            vocab_map['PAD_INDEX'] = 0
            vocab_map['NOT_FOUND_INDEX'] = max_index+1
            vocab_size = len(vocab_map)
            # view vocabulary size and part of the vocabulary map
            print('Vocabulary Size:', vocab_size)
            print('Sample slice of vocabulary map:', dict(list(vocab_map.items())[10:20]))
            from keras.preprocessing import sequence
            from sklearn.preprocessing import LabelEncoder
            max_len = 1445
            test_X = [[vocab_map[token] if vocab_map.get(token) else vocab_map['NOT_FOUND_INDEX']
                    for token in tokenized_review]
                        for tokenized_review in tokenized_test]
            test_X = sequence.pad_sequences(test_X, maxlen=max_len)

            def preprocess_text(text):
                norm_text = tn.normalize_corpus([text])
                tokenized_text = [tn.tokenizer.tokenize(text) for text in norm_text]
                encoded_text = [[vocab_map[token] if vocab_map.get(token) else vocab_map['NOT_FOUND_INDEX']
                                for token in tokenized_review]
                                for tokenized_review in tokenized_text]
                padded_text = sequence.pad_sequences(encoded_text, maxlen=max_len)
                return padded_text
            
            def predict_sentiment(text):
                preprocessed_text = preprocess_text(text)
                predicted_class = trained_model.predict(preprocessed_text)
                return predicted_class
            
            # Example usage:
            res=[['Review','Polarity','Sentiment']]
            for i in self.comm:     
                predicted_sentiment = predict_sentiment(str(i))
                st="Negative" if predicted_sentiment<0.5 else "Positive"
                res.append([i,predicted_sentiment,st])

            # Specify the file path where you want to save the CSV file
            csv_file_path = os.path.abspath('E:/FinalYearProject/FinalYearProject/src/components/output.csv')

            # Write data to CSV file
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(res)

        except Exception as e:
            raise CostumException(e,sys)