import os

from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.post("/url")
def prediction():
    url = request.form["url"]
    return f"url recevived {url}"

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
