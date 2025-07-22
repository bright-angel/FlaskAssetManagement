# -*- encoding: utf-8 -*-

"""
@File    :   generate_data.py
@Time    :   2025/07/20 22:49:33
@Author  :   test233
@Version :   1.0
"""

from app.extensions import db  # 替换为您的应用程序名称
from app.models.asset import Asset  # 替换为您的模型路径
from faker import Faker
from app import create_app
import random

app = create_app()
fake = Faker()

def generate_random_assets(num=100):
    assets = []
    for _ in range(num):
        asset = Asset(
            name=fake.company() + " " + fake.word(),
            category=random.choice(["服务器", "网络设备", "PC", "打印机", "存储设备"]),
            ip_address=fake.ipv4(),
            mac_address=fake.mac_address(),
            os_version=random.choice(["Windows 10", "Ubuntu 20.04", "CentOS 8", "macOS Monterey"]),
            cpu_info=fake.word() + " " + str(random.randint(2, 16)) + "GHz",
            memory=str(random.randint(4, 128)) + "GB",
            storage=str(random.choice([128, 256, 512, 1024])) + "GB",
            value=round(random.uniform(1000, 10000), 2),
            created_by=random.randint(1, 10)  # 假设创建人ID在1到10之间
        )
        assets.append(asset)
    
    return assets

def insert_assets():
    assets = generate_random_assets()
    db.session.bulk_save_objects(assets)
    db.session.commit()
    print(f"成功插入 {len(assets)} 条随机资产数据。")

if __name__ == "__main__":
    with app.app_context():  # 确保在应用上下文中进行操作
        insert_assets()
