FROM python:3.10-slim

WORKDIR /upload_service

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/upload_service

CMD ["python", "cmd/main.py"]
