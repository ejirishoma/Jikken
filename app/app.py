from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
from models import employee
# from models import quiztable

login_manager = LoginManager()
login_manager.init_app(app)

import views

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

    image.save(os.path.join(app.config['IMAGE_UPLOADS'], new_filename+ext))  # save with the new path


if __name__ == '__main__':
    app.run(host='localhost')

