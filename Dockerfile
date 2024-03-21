FROM python:3.12-slim

COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED 1

CMD ["bash"]
