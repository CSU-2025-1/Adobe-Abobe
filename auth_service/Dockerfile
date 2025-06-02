FROM python:3.13-slim

WORKDIR /auth_service

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/auth_service

CMD ["python", "cmd/main.py"]