# -*- encoding: utf-8 -*-

"""
@File    :   forms.py
@Time    :   2025/07/20 22:40:58
@Author  :   test233
@Version :   1.0
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SelectMultipleField,
    SelectField,
    FloatField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from .models import User, Role, Permission


class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("提交")

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField("旧密码", validators=[])
    password = PasswordField("密码", validators=[])
    confirm_password = PasswordField(
        "确认密码", validators=[EqualTo("password", "两次密码不一致")]
    )
    submit = SubmitField("提交")

class UserSearchForm(FlaskForm):
    username = StringField("用户名",render_kw={"placeholder": "用户名"} )
    per_page = SelectField("每页数量", 
                          choices=[(10, '10'), (20, '20'), (50, '50'), (100, '100')], 
                          coerce=int, 
                          default=10)
    search = SubmitField('搜索')
    reset = SubmitField('重置')
class PermissionSearchForm(FlaskForm):
    api = StringField("API端点",render_kw={"placeholder": "API端点"} )
    per_page = SelectField("每页数量", 
                          choices=[(10, '10'), (20, '20'), (50, '50'), (100, '100')], 
                          coerce=int, 
                          default=10)
    search = SubmitField('搜索')
    reset = SubmitField('重置')

class AssetSearchForm(FlaskForm):
    name = StringField("资产名称", render_kw={"placeholder": "资产名称"}, validators=[Optional()])
    category = SelectField("资产类别", 
                           choices=[
                               ('', '所有类别'),  # 默认选项
                               ('服务器', '服务器'), 
                               ('网络设备', '网络设备'), 
                               ('PC', 'PC'), 
                               ('打印机', '打印机'), 
                               ('存储设备', '存储设备')
                           ], 
                           validators=[Optional()])
    ip_address = StringField("IP地址", render_kw={"placeholder": "IP地址"}, validators=[Optional()])
    mac_address = StringField("MAC地址", render_kw={"placeholder": "MAC地址"}, validators=[Optional()])
    per_page = SelectField("每页数量", 
                           choices=[(10, '10'), (20, '20'), (50, '50'), (100, '100')], 
                           coerce=int, 
                           default=10)
    search = SubmitField('搜索')
    reset = SubmitField('重置')

class UserForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(3, 20)])
    password = PasswordField("密码", validators=[])
    confirm_password = PasswordField(
        "确认密码", validators=[EqualTo("password", "两次密码不一致")]
    )
    is_superuser = BooleanField("超级用户")
    roles = SelectMultipleField("角色", coerce=int)
    submit = SubmitField("提交")

    def populate_obj_exclude(self, obj, exclude=None):
        if exclude is None:
            exclude = []
        for field_name, field in self._fields.items():
            if field_name not in exclude:
                setattr(obj, field_name, field.data)

    def populate_obj_exclude(self, obj, exclude=None):
        if exclude is None:
            exclude = []
        for field_name, field in self._fields.items():
            if field_name not in exclude:
                setattr(obj, field_name, field.data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roles.choices = [(r.id, r.name) for r in Role.query.all()]


class RoleForm(FlaskForm):
    name = StringField("角色名", validators=[DataRequired(), Length(2, 20)])
    description = StringField("描述")
    permissions = SelectMultipleField("权限", coerce=int)
    submit = SubmitField("提交")

    def populate_obj_exclude(self, obj, exclude=None):
        if exclude is None:
            exclude = []
        for field_name, field in self._fields.items():
            if field_name not in exclude:
                setattr(obj, field_name, field.data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions.choices = [(p.id, p.endpoint) for p in Permission.query.all()]


class PermissionForm(FlaskForm):
    endpoint = StringField("API端点", validators=[DataRequired()])
    description = StringField("描述")
    submit = SubmitField("提交")


class AssetForm(FlaskForm):
    name = StringField("Asset Name", validators=[DataRequired(), Length(max=100)])
    category = SelectField(
        "Category",
        choices=[
            ("it", "IT Equipment"),
            ("furniture", "Furniture"),
            ("vehicle", "Vehicle"),
            ("other", "Other"),
        ],
    )
    value = FloatField("Value", validators=[DataRequired()])
    submit = SubmitField("提交")
