# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   zhujinchong@foxmail.com
@Author  :   zhujinchong
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/26 10:06    1.0         None
"""
import sys
from pathlib import Path

# 当用python app/main.py启动是，会报错 from app import settings ModuleNotFoundError: No module named 'app'
# 添加项目到Python解释器的系统路径中
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.api import api_test
from app.utils.utils_log import setup_logging, TraceID

# 创建FastAPI应用实例
app = FastAPI(on_startup=[setup_logging])


# 注册路由
def register_router(app: FastAPI):
    app.include_router(api_test.router)


register_router(app)


# 注册中间件
def register_middleware(app: FastAPI):
    # 自定义中间件（日志中记录UUID, 记录错误日志）
    @app.middleware("http")
    async def request_middleware(request: Request, call_next):
        """
        1.设置日志的全链路追踪
        2.记录错误日志
        """
        try:
            REQUEST_ID_KEY = "X-Request-Id"
            _req_id_val = request.headers.get(REQUEST_ID_KEY, "")
            req_id = TraceID.set(_req_id_val)
            logger.info(f"{request.method} {request.url}")
            response = await call_next(request)
            response.headers[REQUEST_ID_KEY] = req_id.get()
            return response
        except Exception as ex:
            logger.exception(ex)  # 这个方法能记录错误栈
            return JSONResponse(content={"success": False}, status_code=500)
        finally:
            pass

    # Gzip压缩，当传输数据量过大时，启动Gzip压缩，提高效率，不影响前端。
    app.add_middleware(
        GZipMiddleware,
        minimum_size=500,  # 启用 Gzip 压缩的最小响应体大小，单位为字节
        compresslevel=6  # Gzip 压缩级别，范围为 0 到 9，级别越高，压缩率越高，但耗费的 CPU 越多
    )

    # 跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
        allow_credentials=False,  # 是否允许携带凭证（例如，使用 HTTP 认证、Cookie 等）
        allow_methods=["*"],  # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
        allow_headers=["*"],
        # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头。当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
        # expose_headers=["*"],  # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
        # max_age=1000  # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    )


register_middleware(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.IP, port=settings.PORT, workers=1)
