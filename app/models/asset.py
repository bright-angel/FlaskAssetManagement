# -*- encoding: utf-8 -*-

"""
@File    :   asset.py
@Time    :   2025/07/20 22:49:33
@Author  :   test233
@Version :   1.0
"""

from ..extensions import db
from datetime import datetime


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    crearted_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("assets", lazy=True))
