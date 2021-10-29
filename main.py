from flask import Flask, render_template, request, redirect, session, jsonify
from flask.helpers import make_response
import mysql.connector
import os
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import pickle

app = Flask(__name__)
app.secret_key = os.urandom(10)
loaded_model = pickle.load(open("model.pkl", "rb"))
cv = pickle.load(open("vectors.pkl", "rb"))

@app.route('/')
def home():
  msg=""
  return render_template('home.html',msg=msg)

def remove_special_char(text):
    new_text = ""
    for i in text.split():
        if i.isalpha():
            new_text = new_text + " " + i
        
    return new_text

@app.route('/result', methods=['POST'])
def result():
  mail = request.form.get('mail')
  mail=str(mail)
  print(mail)
  msg=""
  if(mail!="" ):
    mail=mail.lower()
    mail=mail.replace('\n', " ")
    mail=mail.replace('\t', " ")
    mail=remove_special_char(mail)
    result=loaded_model.predict(cv.transform([mail]).toarray())[0]
    if result==0:
        msg="Ham"
    else:
        msg="Spam"
      
  return render_template('home.html',msg=msg)

if __name__ == '__main__':
  app.run(debug=True)
