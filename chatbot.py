from mysql.connector.utils import intstore
import nltk
from nltk import internals
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

import sys

from tensorflow.keras.models import load_model
model = load_model('./trainingChatbot/chatbot_model.h5')
import json
import random
intents = json.loads(open('./trainingChatbot/intents.json').read())
words = pickle.load(open('./trainingChatbot/words.pkl','rb'))
classes = pickle.load(open('./trainingChatbot/classes.pkl','rb'))


import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.tree import export_graphviz
import warnings
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning)

import mysql.connector
import datetime

cnx = mysql.connector.connect(host="localhost", database="chatbot", user="root", password="ayush10301")


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):

    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg, ints):
    cursor = cnx.cursor()
    if(ints[0]['intent'] == 'scheduling_help'):
        cursor.execute("SELECT admins.name AS name, appointments.date AS date, appointments.time AS time FROM admins INNER JOIN appointments ON appointments.admin_id=admins.id WHERE appointments.user_id IS NULL ORDER BY name, date, time;")
        answer = "Message me any of the following to schedule a meeting:\n\n"
        for(name, date, time) in cursor:
            answer += name + " : " + date.strftime('%Y/%m/%d') + " - " + str(time) + "\n"
        cursor.close()
        return answer

    if(ints[0]['intent'] == 'cancel_appointments'):
        cursor.execute("UPDATE appointments SET user_id=NULL WHERE user_id IS NOT NULL;")
        cursor.close()

    if(ints[0]['intent'] == 'show_appointments'):
        cursor.execute("SELECT admins.name AS name, appointments.date AS date, appointments.time AS time FROM admins INNER JOIN appointments ON appointments.admin_id=admins.id WHERE appointments.user_id=1 ORDER BY name, date, time;")
        result = cursor.fetchall()
        if(len(result)==0):
            return "You don't have any appointments"
        answer = "You have the following appointments:\n\n"
        for(name, date, time) in result:
            answer += name + " : " + date.strftime('%Y/%m/%d') + " - " + str(time) + "\n"
        cursor.close()
        return answer

    if(msg['schedule']):
        query = "UPDATE appointments SET user_id=1 WHERE admin_id=(SELECT a.id FROM admins AS a WHERE a.name='"+msg['name']+"') AND date='"+msg['date']+"' AND time='"+msg['time']+"';"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        return "Your meeting has been scheduled"
        
    cursor.close()
    res = getResponse(ints, intents)
    return res

