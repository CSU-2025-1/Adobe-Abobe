FROM python:3.11

WORKDIR /api_gateway

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "cmd/main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
