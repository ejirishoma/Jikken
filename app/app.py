from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='localhost')

@app.route('/')
def index():
        return 'Hellow World!'
