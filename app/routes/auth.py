# -*- encoding: utf-8 -*-

"""
@File    :   auth.py
@Time    :   2025/07/20 22:43:28
@Author  :   test233
@Version :   1.0
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user,current_user
from ..forms import LoginForm,UserForm1
from ..models import User
from ..extensions import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("登录成功", "success")
            return redirect(url_for("main.index"))
        flash("用户名或密码错误", "danger")
    return render_template("auth/login.html", form=form)

@bp.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    user = User.query.get_or_404(current_user.id)
    form = UserForm1(obj=user)
    if form.validate_on_submit():
        form.populate_obj_exclude(user, exclude=["username"])
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("用户更新成功", "success")
        return redirect(url_for("main.index"))
    form.roles.data = [role.id for role in user.roles]
    return render_template(
        "edit_user.html", form=form, user=user, title="编辑用户"
    )


@bp.route("/logout")
def logout():
    logout_user()
    flash("您已登出", "info")
    return redirect(url_for("auth.login"))
