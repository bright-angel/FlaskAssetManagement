# -*- encoding: utf-8 -*-

'''
@File    :   run.py
@Time    :   2025/07/20 22:50:56
@Author  :   test233
@Version :   1.0
'''

from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)