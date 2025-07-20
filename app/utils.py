# -*- encoding: utf-8 -*-

"""
@File    :   utils.py
@Time    :   2025/07/20 22:41:13
@Author  :   test233
@Version :   1.0
"""

from werkzeug.security import generate_password_hash
from functools import wraps
from flask import abort, current_app
from flask_login import current_user, login_required
from .models import Role, User
from .extensions import db


def permission_required(endpoint):
    """
    权限校验装饰器
    :param endpoint: 权限端点
    """

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            # 如果是超级用户，直接放行
            if current_user.is_superuser:
                return f(*args, **kwargs)

            if not current_user.has_permission(endpoint):
                # 记录详细的权限拒绝日志
                current_app.logger.warning(
                    f"Permission denied: user={current_user.username}, "
                    f"endpoint={endpoint}"
                )
                abort(403)  # 返回 403 Forbidden

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_required(role_name):
    """角色校验装饰器"""

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            # 如果是超级用户，直接放行
            if current_user.is_superuser:
                return f(*args, **kwargs)

            # 检查角色
            if not current_user.has_role(role_name):
                current_app.logger.warning(
                    f"Role required: user={current_user.username}, "
                    f"required_role={role_name}"
                )
                abort(403)  # 返回 403 Forbidden

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def any_role_required(*role_names):
    """多角色校验装饰器（拥有任意一个角色即可）"""

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            # 如果是超级用户，直接放行
            if current_user.is_superuser:
                return f(*args, **kwargs)

            # 检查是否有任意角色
            if not any(current_user.has_role(role) for role in role_names):
                current_app.logger.warning(
                    f"Any role required: user={current_user.username}, "
                    f"required_roles={', '.join(role_names)}"
                )
                abort(403)  # 返回 403 Forbidden

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """管理员校验装饰器（便捷方法）"""

    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # 检查管理员角色或超级用户
        if not (current_user.is_superuser or current_user.has_role("admin")):
            current_app.logger.warning(f"Admin required: user={current_user.username}")
            abort(403)  # 返回 403 Forbidden

        return f(*args, **kwargs)

    return decorated_function


# 权限管理工具类
class RBACManager:
    @staticmethod
    def initialize_roles():
        """初始化系统角色"""
        roles = {
            "sysadmin": "系统管理员",
            "projadmin": "项目管理员",
            "member": "项目成员",
        }

        for name, desc in roles.items():
            if not Role.query.filter_by(name=name, description=desc).first():
                role = Role(name=name, description=desc)
                db.session.add(role)
        db.session.commit()

    @staticmethod
    def create_admin_user(username, password):
        """创建管理员用户"""
        admin_role = Role.query.filter_by(name="sysadmin").first()
        if not admin_role:
            admin_role = Role(name="sysadmin")
            db.session.add(admin_role)

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                password=generate_password_hash(password),
                is_superuser=True,
            )
            user.roles.append(admin_role)
            db.session.add(user)
            db.session.commit()
        return user
