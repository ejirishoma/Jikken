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