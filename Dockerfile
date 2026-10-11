FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]