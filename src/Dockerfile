FROM python:3.9-slim
COPY requirements.txt .
RUN --mount=type=cache,target=/root/cache/.pip pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD kopf run --standalone /app/operator_handler.py