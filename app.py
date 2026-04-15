import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()  # converting every text in to lowercase
    text = nltk.word_tokenize(text)  # tokenizing each word and storing each word in text as list element

    y = []
    for i in text:
        if i.isalnum():  # filtering out alphabets and numbers and removing special symbols in the text
            y.append(i)

    text = y[
        :]  # this is done to avoid sharing same memory of different variable i.e. if we do text = y, then copy of memory is done and any update in y will change text to
    y.clear()  # clearing to reuse it

    for i in text:
        if i not in stopwords.words(
                'english') and i not in string.punctuation:  # filtering out from stopwords and punctuations
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))  # stemming each word i.e. love, loved, loving are all same word i.e. love
    return " ".join(y)  # returning in the form of string


tfidf = pickle.load(open('models/vectorizer.pkl','rb')) #opening in read binary mode
model = pickle.load(open('models/model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    # 1. preprocess
    transform_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transform_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.error("### 🚨 ALERT: Spam!")
    else:
        st.success("### ✅ Safe: Not Spam!")

# --- FOOTER ---
st.caption("Developed by PANCHAJANYA RAY | Focus: Email & SMS Classifier")