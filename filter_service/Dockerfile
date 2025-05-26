FROM python:3.13-slim

WORKDIR /filter_service

RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/filter_service

CMD ["python", "cmd/main.py"]
