FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

RUN pip install fastapi uvicorn httpx jinja2 python-multipart

RUN chmod +x start.sh

CMD ["./start.sh"]