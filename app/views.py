from flask import render_template, request, redirect, url_for
from app import db
from app import app
from random import randint
from flask_login import UserMixin, LoginManager, login_user , logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.employee import User_info

@app.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        user = User_info.query.get(user_id)
        return render_template('testapp/student_login.html', user=user)
    else:
        return redirect('/login')  

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User_info(name=username, password=generate_password_hash(password, method='sha256'))
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
    roomname = request.form.get('room')
    user_id = current_user.get_id()
    user = User_info.query.get(user_id)
    return render_template('testapp/QuizRoom.html', roomname=roomname, user=user)

    