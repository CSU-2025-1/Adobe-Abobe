FROM python:3.13-slim

WORKDIR /filter_service

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/filter_service

CMD ["python", "cmd/main.py"]
