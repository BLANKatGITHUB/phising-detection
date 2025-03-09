import os

from flask import Flask, render_template,request

import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__)
max_len = 104

model = tf.keras.models.load_model("phishing_model.h5")
# Load the tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)

@app.route("/")
def index():
    return render_template('index.html')

@app.post("/url")
def prediction():
    url = request.form["url"]
    url_sequence = loaded_tokenizer.texts_to_sequences([url])
    url_padded = pad_sequences(url_sequence, maxlen=max_len,padding="post")
    prediction = model.predict(url_padded)

    value = prediction.round()

    if value == 1:
        prediction = "Legitmate"
    else:
        prediction = "Phising"

    return render_template('index.html',prediction=prediction)

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
