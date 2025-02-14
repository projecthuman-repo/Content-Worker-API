import pandas as pd
import numpy as np
import re
import string
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

data=pd.read_csv("labeled_data.csv") #Update the file path here
print(f"Data loaded with {data.shape[0]} rows and {data.shape[1]} columns.")
tweets=data["tweet"]
categories=data["class"].astype(int)
print(f"Text data and labels extracted. Total samples: {len(tweets)}.")

stop_words=set(stopwords.words("english"))
stemmer=PorterStemmer()
sentiment_analyzer=SentimentIntensityAnalyzer()

def preprocess_text(text):
    text=re.sub(r"http\S+","",text)
    text=re.sub(r"@\w+","",text)
    text=text.lower().translate(str.maketrans("","",string.punctuation))
    return text

def tokenize_text(text):
    tokens=text.split()
    return[stemmer.stem(word)for word in tokens if word not in stop_words]

def get_text_features(text):
    processed_text=preprocess_text(text)
    sentiment_scores=sentiment_analyzer.polarity_scores(processed_text)
    char_count=len(processed_text)
    word_count=len(processed_text.split())
    return[char_count,word_count,sentiment_scores["neg"],sentiment_scores["pos"],sentiment_scores["neu"],sentiment_scores["compound"]]

features=np.array([get_text_features(text)for text in tweets])
print(f"Extracted features from {len(features)} texts.")
train_tweets,test_tweets,train_categories,test_categories,train_features,test_features=train_test_split(tweets,categories,features,test_size=0.2,random_state=42,stratify=categories)
print(f"Data split into training and testing sets. Training set size: {len(train_tweets)}, Testing set size: {len(test_tweets)}.")

vectorizer=TfidfVectorizer(tokenizer=tokenize_text,preprocessor=preprocess_text,max_features=5000)
train_vectors=vectorizer.fit_transform(train_tweets).toarray()
test_vectors=vectorizer.transform(test_tweets).toarray()
print(f"TF-IDF vectorization complete. Training vector size: {train_vectors.shape}, Testing vector size: {test_vectors.shape}.")

train_dataset=np.hstack((train_vectors,train_features))
test_dataset=np.hstack((test_vectors,test_features))
classifier=LogisticRegression(class_weight="balanced",solver="liblinear",C=1.0)
print("Training Logistic Regression model.")

classifier.fit(train_dataset,train_categories)
predictions=classifier.predict(test_dataset)
print("Model trained. Predicting test set labels.")
print(classification_report(test_categories,predictions))

conf_matrix=confusion_matrix(test_categories,predictions,normalize="true")
plt.figure(figsize=(6,5))
sns.heatmap(conf_matrix,annot=True,fmt=".2f",cmap="Blues",xticklabels=["Hate","Spam","Safe"],yticklabels=["Hate","Spam","Safe"])
plt.xlabel("Predicted Categories")
plt.ylabel("True Categories")
plt.show()
