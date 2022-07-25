from flask import render_template, request, redirect, url_for
from app import db
from app import app
from random import randint, randrange
from flask_login import UserMixin, LoginManager, login_user , logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.employee import User_info
from models.quiztable import quiz_info
import random
import os
import string

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        user_data = User_info.query.get(user_id)

        if (user_data.zokusei == 0):
            return redirect('/student_login')
        else:
            return redirect('/teacher_login')
    else:
        return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        job = request.form.get('zokusei')
        username = request.form.get('name')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User_info(zokusei = job, name=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('testapp/signup.html')

@app.login_manager.user_loader
def load_user(user_id):
    return User_info.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User_info.query.filter(User_info.name == username).first()
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect('/')
    else:
        return render_template('testapp/login.html')
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/Quizroom', methods=['GET', 'POST'])
@login_required
def Quizroom():
    # roomname = request.form.get('room')
    user_id = current_user.get_id()
    user = User_info.query.get(user_id)

    # if request.method == "POST":
    id_count = db.session.query(quiz_info).count()
    random_id = random.randrange(0, id_count, 1)
    quiz_data = quiz_info.query.get(random_id)

    return render_template('testapp/QuizRoom.html', quiz_data=quiz_data, user=user)

@app.route('/makequiz', methods=['GET', 'POST'])
@login_required
def makequiz():
    user_id = current_user.get_id()
    user_data = User_info.query.get(user_id)
    if (user_data.zokusei == 1):
        if request.method == "POST":
            questionid = request.form.get('questionid')
            sentence = request.form.get('sentence')
            choice1 = request.form.get('Choice1')
            choice2 = request.form.get('Choice2')
            choice3 = request.form.get('Choice3')
            choice4 = request.form.get('Choice4')
            answer = request.form.get('answer')
            file_name = request.form.get('link')
            # if not allowed_images(image.filename):
            #     return redirect(request.url)
            # else:
            ext = os.path.splitext(file_name)[1]  # get the file extension
            new_filename = get_random_string(20)  # create a random string

            image.save(os.path.join(app.config['IMAGE_UPLOADS'], new_filename+ext))  # save with the new path

            quiz = quiz_info(questionid = questionid, sentence=sentence, Choice1=choice1, Choice2=choice2, Choice3=choice3, Choice4=choice4, link=os.path.join(app.config['IMAGE_UPLOADS'], new_filename+ext))
            
            # if(user_data.questionid == questionid):#問題IDが被ったら上書きする
            #     db.session.merge(quiz)
            #     db.session.commit()
            # else:
            db.session.add(quiz)
            db.session.commit()

            return redirect('/')
        
        else: 
           return render_template('testapp/makequiz.html')
    else:
        return redirect('/')

@app.route('/student_login', methods=['GET', 'POST'])
@login_required
def student_login():
    user_id = current_user.get_id()
    user_data = User_info.query.get(user_id)

    return render_template('testapp/student_login.html', user=user_data)

@app.route('/teacher_login')
@login_required
def teacher_login():
    user_id = current_user.get_id()
    user_data = User_info.query.get(user_id)

    return render_template('testapp/teacher_login.html', user=user_data)