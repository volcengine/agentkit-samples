FROM agentkit-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim_v1031_1

ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1 DOCKER_CONTAINER=1

WORKDIR /app

# 复制项目文件
COPY . .

# 安装基础依赖
RUN uv pip install -r requirements.txt

CMD ["python", "-m", "agent"]
