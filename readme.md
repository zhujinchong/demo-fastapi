> 最后修改时间：2024/12/30

# 项目运行

1. 安装环境

```shell
pip install fastapi uvicorn loguru pydantic requests
# 或
poetry install --without dev
```

2. 修改配置

```shell
vi app/settings.py
```

3. 启动

```shell
python app/main.py
或
uvicorn app.main:app --host='0.0.0.0' --port=8000 --workers=1
```

# Docker运行

Dockerfile 参考 https://blog.csdn.net/2201_75632987/article/details/142000817

```shell
# 构建镜像
docker build -t myapp .
# 运行
docker run -itd --name myapp -p 18888:8000 -v ./logs:/workdir/logs --restart=always myapp 
```

# 测试

```shell
curl http://localhost:18888/ai/test
```

# 参考poetry命令

```shell
# 进入conda环境，略
# 进入项目，略

# 安装poetry
pip install poetry

# 配置镜像源（可选，国内用户推荐）
poetry config repositories.tsinghua https://pypi.tuna.tsinghua.edu.cn/simple

# 第一次：在项目中初始化
poetry init

# 安装项目依赖
poetry install

# 添加新依赖
poetry add requests pandas

# 添加开发依赖
poetry add --group dev pytest
```
