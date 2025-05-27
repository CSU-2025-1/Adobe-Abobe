FROM python:3.10-slim

WORKDIR /story_service

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/story_service

CMD ["python", "cmd/main.py"]
