from flask import Flask
from flask import render_template

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='localhost')

@app.route('/')
def index():
        return render_template('testapp/index.html')
