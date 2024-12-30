# -*- encoding: utf-8 -*-
"""
@File    :   settings.py    
@Contact :   zhujinchong@foxmail.com
@Author  :   zhujinchong
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/26 10:06    1.0         None
"""
from pathlib import Path

# 项目根目录 /
BASE_DIR = Path(__file__).parent.parent.absolute()
# 项目IP
IP = '0.0.0.0'
# 项目端口
PORT = 8000
# 日志级别
DEBUG = False
