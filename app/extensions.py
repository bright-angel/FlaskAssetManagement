# -*- encoding: utf-8 -*-

"""
@File    :   extensions.py
@Time    :   2025/07/20 22:40:43
@Author  :   test233
@Version :   1.0
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


@login_manager.user_loader
# 定义一个函数，用于加载用户
def load_user(user_id):
    # 从app.models.user模块中导入User类
    from .models import User

    return User.query.get(int(user_id))
