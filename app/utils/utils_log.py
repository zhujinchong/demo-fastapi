# -*- encoding: utf-8 -*-
"""
@File    :   utils_log.py
@Contact :   zhujinchong@foxmail.com
@Author  :   zhujinchong
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/27 10:48    1.0         None
"""

import os
from pathlib import Path

from loguru import logger

from app import settings


def setup_logging():
    """
    配置日志系统
    """
    # 步骤1：移除默认处理器
    logger.configure(extra={"request_id": ''})  # Default values 否则会报错
    logger.remove()

    # 步骤2：定义日志格式
    log_format = (
        # 时间信息 + UUID
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[request_id]} | "
        # 日志级别，^居中对齐 8是指定宽度
        "<level>{level: ^8}</level> | "
        # 进程和线程信息
        "process [<cyan>{process}</cyan>]:<cyan>{thread}</cyan> | "
        # 文件、函数和行号
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        # 日志消息
        "<level>{message}</level>"
    )

    # 步骤3：创建日志目录
    log_dir = Path(settings.BASE_DIR, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 步骤4：配置常规日志文件
    logger.add(
        str(Path(log_dir, "log.log")),
        format=log_format,
        level="INFO",
        rotation="10 MB",
        retention="1000 days",
        encoding="utf-8",
        enqueue=True,  # 异步写入
    )
