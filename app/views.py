from flask import render_template, request, redirect, url_for, flash
from app import db
from app import app
from random import randint, randrange
from flask_login import UserMixin, LoginManager, login_user , logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.employee import User_info
from models.quiztable import quiz_info
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy.sql import func
import random
import os
import string

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    id_count = db.session.query(func.count(quiz_info.questionid)).scalar()
    random_id = random.randint(1,id_count)
    quiz_data = quiz_info.query.get(random_id)

    form_answer = request.form.get('answer')
    db_answer = quiz_info.query.get(random_id).answer
    if request.method == "POST":
        if(int(form_answer) == db_answer):
            flash('正解です')
        else:
            flash('不正解です')
    
    return render_template('testapp/QuizRoom_sub.html', quiz_data=quiz_data, user=user)

@app.route('/makequiz', methods=['GET', 'POST'])
@login_required
def makequiz():
    user_id = current_user.get_id()
    user_data = User_info.query.get(user_id)
    if (user_data.zokusei == 1):
        if request.method == "POST":
            file = request.files['link']

            if file and allwed_file(file.filename):
                # 危険な文字を削除（サニタイズ処理）
                filename = secure_filename(file.filename)
                # ファイルの保存
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # アップロード後のページに転送
                # return redirect(url_for('uploaded_file', filename=filename))
            

            questionid = request.form.get('questionid')
            sentence = request.form.get('sentence')
            choice1 = request.form.get('Choice1')
            choice2 = request.form.get('Choice2')
            choice3 = request.form.get('Choice3')
            choice4 = request.form.get('Choice4')
            answer = request.form.get('answer')
            file_name = filename

            quiz = quiz_info(questionid = questionid, sentence=sentence, Choice1=choice1, Choice2=choice2, Choice3=choice3, Choice4=choice4, link=file_name, answer=answer)
        
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


@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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

@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def unauthorized(error):
    return redirect(url_for('index'))
