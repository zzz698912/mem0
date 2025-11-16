FROM registry.cn-hangzhou.aliyuncs.com/yuanzhang-images/python:3.12-slim

LABEL org.opencontainers.image.name="mem0/openmemory-mcp"


# 复制 mem0 目录结构（用于构建时）
COPY mem0 /usr/src/mem0

WORKDIR /usr/src/openmemory

COPY requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY config.json .
COPY . .

EXPOSE 8765
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8765"]