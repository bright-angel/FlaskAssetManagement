# -*- encoding: utf-8 -*-

"""
@File    :   user.py
@Time    :   2025/07/20 22:49:14
@Author  :   test233
@Version :   1.0
"""

from ..extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# --- 关联表 ---
user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)

role_permission = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True
    ),
)


# --- 核心模型 ---
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_superuser = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 多对多关系
    roles = db.relationship("Role", secondary=user_role, back_populates="users")

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def has_role(self, role_name):
        """检查用户是否拥有指定角色"""
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, endpoint):
        """检查用户是否有指定权限"""
        if self.is_superuser:
            return True

        # 优化查询：通过单次连接查询检查权限
        from sqlalchemy import exists

        return db.session.query(
            exists().where(
                user_role.c.user_id == self.id,
                role_permission.c.role_id == user_role.c.role_id,
                role_permission.c.permission_id == Permission.id,
            )
        ).scalar()

    def update_roles(self, role_ids):
        """更新用户的角色"""
        # 获取当前角色ID集合
        current_ids = {role.id for role in self.roles}
        target_ids = set(role_ids)

        # 添加新角色
        for rid in target_ids - current_ids:
            role = Role.query.get(rid)
            if role:
                self.roles.append(role)

        # 移除旧角色
        for rid in current_ids - target_ids:
            role = Role.query.get(rid)
            if role:
                self.roles.remove(role)

        db.session.commit()


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 多对多关系
    users = db.relationship("User", secondary=user_role, back_populates="roles")
    permissions = db.relationship(
        "Permission", secondary=role_permission, back_populates="roles"
    )

    def has_permission(self, endpoint):
        """检查角色是否有指定权限"""
        return (
            Permission.query.join(role_permission)
            .filter(
                role_permission.c.role_id == self.id, Permission.endpoint == endpoint
            )
            .first()
            is not None
        )


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 多对多关系
    roles = db.relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )
