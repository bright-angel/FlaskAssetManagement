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
    __tablename__ = "asset"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment="资产名称")
    category = db.Column(db.String(50), nullable=False, comment="资产类别(服务器/网络设备/PC等)") 
    ip_address = db.Column(db.String(50), comment="IP地址")
    mac_address = db.Column(db.String(50), comment="MAC地址")
    os_version = db.Column(db.String(100), comment="操作系统版本")
    cpu_info = db.Column(db.String(100), comment="CPU信息")
    memory = db.Column(db.String(50), comment="内存容量")
    storage = db.Column(db.String(50), comment="存储容量")
    value = db.Column(db.Float, comment="资产价值")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="创建人ID")
