import os

from flask import Flask, render_template,request


import pickle




app = Flask(__name__)

filename = 'lr_model.pkl'
with open(filename, 'rb') as file:
    loaded_model = pickle.load(file)


def preprocessing(url):
    url_length = len(url)
    dot_count = url.count(".")
    slash_count = url.count("/")
    dash_count = url.count("-")
    underscore_count = url.count("_")
    at_count = url.count("@")
    question_count = url.count("?")
    equal_count = url.count("=")
    and_count = url.count("&")
    digit_count = sum(c.isdigit() for c in url)
    letter_count = sum(c.isalpha() for c in url)
    has_http = int("http" in url)
    has_https = int("https" in url)
    has_www = int("www" in url)

    return [
        url_length,
        dot_count,
        slash_count,
        dash_count,
        underscore_count,
        at_count,
        question_count,
        equal_count,
        and_count,
        digit_count,
        letter_count,
        has_http,
        has_https,
        has_www,
    ]


@app.route("/")
def index():
    return render_template('index.html')

@app.post("/url")
def prediction():
    url = request.form["url"]
    
    x = preprocessing(url)
    value = loaded_model.predict([x])

    if value == 1:
        prediction = "Legitmate"
    else:
        prediction = "Phising"

    return render_template('index.html',prediction=prediction)

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
