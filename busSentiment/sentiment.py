from joblib import load
from nltk.tokenize import RegexpTokenizer
import os

currentDir = os.getcwd() + "/busSentiment"
loaded_model = load(currentDir+"/MySecondNLPModel.joblib")
loaded_vectorizer = load(currentDir+"/myFirstVectorizer.joblib")

def busSentimentModule(text):

    # The bus is maintained top notch
    # The maintenance of the bus is excellent
    token = RegexpTokenizer(r'[a-zA-Z0-9]+')
    new_text_tokens = token.tokenize(text)

    new_text_features = loaded_vectorizer.transform([' '.join(new_text_tokens)])


    predicted_sentiment = loaded_model.predict(new_text_features)[0]
    return predicted_sentiment
