# -*- encoding: utf-8 -*-

"""
@File    :   __init__.py
@Time    :   2025/07/20 22:40:25
@Author  :   test233
@Version :   1.0
"""

from .config import Config
from .extensions import db, login_manager, migrate, csrf
from .routes import main, auth, asset, admin
from .models import Permission
from .utils import RBACManager

from flask import Flask
from flask_bootstrap import Bootstrap5


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bootstrap = Bootstrap5(app)
    csrf.init_app(app)

    # 注册蓝图
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(asset.bp)
    app.register_blueprint(admin.bp)

    # 在应用上下文中初始化数据库并创建默认角色和管理员
    with app.app_context():
        # 创建数据库表（如果不存在）
        db.create_all()
        # 初始化RBAC
        RBACManager.initialize_roles()
        # 创建默认管理员用户
        RBACManager.create_admin_user(
            app.config.get("ADMIN_USERNAME", "admin"),
            app.config.get("ADMIN_PASSWORD", "adminpassword"),
        )
        for rule in app.url_map.iter_rules():
            existing = Permission.query.filter_by(endpoint=rule.endpoint).first()
            if not existing:
                permission = Permission(endpoint=rule.endpoint)
                db.session.add(permission)
        # 提交所有更改
        db.session.commit()

    return app
