from app import db
from datetime import datetime
from flask_login import UserMixin

class User_info(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    zokusei = db.Column(db.Integer) # 生徒なら0、教師なら1
    name = db.Column(db.String(255))  # 社員名
    password = db.Column(db.String(255)) # パスワード
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class quiz_info(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    questionid = db.Column(db.Integer)#問題ID
    sentence = db.Column(db.String(511))  # 問題文
    Choice1 = db.Column(db.String(10))  # 選択肢1
    Choice2 = db.Column(db.String(10))  # 選択肢2
    Choice3 = db.Column(db.String(10))  # 選択肢3
    Choice4 = db.Column(db.String(10))  # 選択肢4
    answer = db.Column(db.Integer) #正解の選択肢
    link = db.Column(db.String(30))#画像のパス名