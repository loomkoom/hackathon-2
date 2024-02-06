import random
import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class Model:
    def __init__(self, path) -> None:
        self.classes = ['PP','PO','UN']
        self.df = self.__load_file(path)
        self.target = None
        self.model = None
        self.input = None
        # self.X_train_full = None
        # self.X_test_full = None
        # self.y_train = None
        # self.y_test = None

    def __load_file(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        return df

    def prepare_data(self):
        self.df.drop(['A1', 'A2', 'A3', 'A4', 'A5', 'A6'], inplace=True, axis=1)
        self.df.drop(['roundID'], inplace=True, axis=1)

        self.df = self.df[self.df['majority_vote'] != "NoMajority"]
        # self.df.reset_index(drop=True, inplace=True)

        self.target = self.df['majority_vote']
        self.df.drop(['majority_vote'], inplace=True, axis=1)
        
        # X_train, X_test, self.y_train, self.y_test = train_test_split(
        #     self.df, target, test_size=0.2, random_state=42)
        
        # X_train_tweet = X_train["proc_text"]
        # X_test_tweet = X_test["proc_text"]
        # X_train.drop(['proc_text',"text"],inplace=True,axis=1)
        # X_test.drop(['proc_text',"text"],inplace=True,axis=1)

        tf_id_vectorizer = TfidfVectorizer(stop_words='english',min_df=0.01,max_df=0.9)
        tweet_tfid = tf_id_vectorizer.fit_transform(self.df["proc_text"])
        self.df.drop(['proc_text',"text"],inplace=True,axis=1)
        
        # X_train_tweet_tfid = tf_id_vectorizer.fit_transform(X_train_tweet)
        # X_test_tweet_tfid = tf_id_vectorizer.transform(X_test_tweet)
        
        # self.X_train_full = np.concatenate((X_train,X_train_tweet_tfid.toarray()),axis=1)
        # self.X_test_full = np.concatenate((X_test,X_test_tweet_tfid.toarray()),axis=1)
        
        self.input = np.concatenate((self.df,tweet_tfid.toarray()),axis=1)

    def train_randomforest(self):
        # Best parameters found by grid search: {'max_depth': 20, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 200}
        rf = RandomForestClassifier(
            max_depth=20, min_samples_leaf=1, min_samples_split=2, n_estimators=200)
        rf.fit(self.df, self.target)

        self.model = rf

    def predict(self, idx):
        pred = self.model.predict(self.df.iloc[[idx]])
        return self.classes.index(pred[0])

model = Model('data/r1_r2_annotations_liwc_h.xlsx')
model.prepare_data() 
model.train_randomforest()
for _ in range(len(model.df)-1):
    i = random.randint(0, len(model.df)-1)
    print(model.predict(i))