#Importing libraries
import flask
from flask import request, jsonify, render_template
from flask_cors import CORS, cross_origin
import base64
import io
import pandas as pd

app = flask.Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    #Render index.html page
    return render_template('index.html')

#API to get the related results by taking the question string as input
@app.route('/question',methods=['POST'])
@cross_origin()
def find_answer():
    request_data = request.get_json()
    string = request_data['question']

    response = jsonify(answer=qna2(string))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def qna2(string):
    import re
    import spacy

    #Checking if the question is an empty string
    if len(string) < 1:
        return [{"fileName":"", "pageNumber":"",
        "content":"Please enter a question"}]

    #Loading the saved dataframe 
    sentences_df = pd.read_pickle("sentences_df.pkl")
    #Loading spacy
    nlp = spacy.load('en_core_web_sm')

    #Converting the input string into tokens and removing punctuations
    qtoken = [token.lemma_.lower() for token in nlp(string) if not token.is_punct]

    #Comparing the count of tokens from questions in each sentence and storing the count
    sentences_df["op"] = sentences_df["processed"].apply(lambda x : sum(token in x for token in qtoken))
    
    #Checking the maximum value of token found in the sentences dataframe
    count = max(sentences_df["op"].sort_values(ascending=False))

    #Creating empty list for the output
    op = []

    #Checking more than 2 tokens are found in the sentences
    if count>1:
        matched_df = sentences_df[["file","page","content"]][sentences_df["op"]==count]
        
        op = []
        for index,row in matched_df.iterrows():
            content = row[2].replace("\u2022", "<br> \u2022")
            op.append({"fileName":row[0], "pageNumber":int(row[1]),"content":content})
    else:
        op.append({"fileName":"", "pageNumber":"",
        "content":"No matching results found. Please try asking the question differently"})
    
    return(op)

def qna(string):
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument
    from nltk.tokenize import word_tokenize
    model = Doc2Vec.load("doc2vec")
    sentences_df = pd.read_pickle("sentences_df.pkl")

    def doc2vec_sim(model,question):
        q_token = word_tokenize(question.lower())
        q_vec = model.infer_vector(q_token)
        sim = model.docvecs.most_similar([q_vec], topn=len(model.docvecs))
        sim_filter = [int(line[0]) for line in sim][0:10]
        return [sentences_df.iloc[i-1:i+2] for i in sim_filter]

    match = doc2vec_sim(model,string)

    op = []
    for item in match:
        file = item["file"].values[0]
        page = item["page"].values[0]
        content = item["content"].values[0] + "<mark>"+ item["content"].values[1] + "</mark>" + item["content"].values[2]
        
        op.append({"fileName":file, "pageNumber":int(page),"content":content})

    return((op))


if __name__ == '__main__':
    app.run()

