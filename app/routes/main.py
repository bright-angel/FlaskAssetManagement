# -*- encoding: utf-8 -*-

"""
@File    :   main.py
@Time    :   2025/07/20 22:43:16
@Author  :   test233
@Version :   1.0
"""

from flask import Blueprint, render_template
from flask_login import current_user

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html", user=current_user)
