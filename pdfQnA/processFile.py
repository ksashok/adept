#Reads a pdf file and performs processing to be used by app.py

import fitz
import pandas as pd
from textblob import TextBlob
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import re
import spacy

#Function to extract pdf file using fitz
def extractText(file): 
    doc = fitz.open(file) 
    text = []
    for i,page in enumerate(doc): 
        t = page.getText() 
        text.append([i+1,t])
    return text

filepath = "TO BE UPDATED"

data = extractText(filepath)

#Converting the list of lists to a dataframe
df = pd.DataFrame(data,columns=['page',"content"])


sentences_list = []
for index,row in df.iterrows():
    #TO-DO : Update file name
    file = "consumer-lending-tc.pdf"
    blob = TextBlob(row["content"])
    for sentence in blob.sentences:
        sentences_list.append([file,row["page"],sentence.raw])

#Dataframe to hold the sentences with filename and corresponding page number
sentences_df = pd.DataFrame(sentences_list,columns=['file','page',"content"])

#Removing the sentences which are less than 10 characters
sentences_df = sentences_df[sentences_df["content"].apply(len)>10].reset_index(drop=True)

#Removing empty spaces from the content
sentences_df = sentences_df[sentences_df["content"].apply(lambda x: len(x.split(' ')))>3]

#Removing all characters which are not alphanumeric
sentences_df["processed"] = sentences_df["content"].apply(lambda x : re.sub(r'[^\w]', ' ', x))

#Removing all stopwords, converting into lowercase and removing empty spaces
sentences_df["processed"] = sentences_df["processed"].apply(lambda x : [token.lemma_.lower() for token in nlp(x) if not token.is_stop and not token.is_space])

#Storing the dataframe object as a pickle
sentences_df.to_pickle("sentences_df.pkl")