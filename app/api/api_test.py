# -*- encoding: utf-8 -*-
"""
@File    :   api_test.py.py    
@Contact :   zhujinchong@foxmail.com
@Author  :   zhujinchong
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/26 16:51    1.0         None
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/ai/test")
def server_test():
    return True
