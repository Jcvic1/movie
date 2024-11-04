FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y postgresql-client && chmod +x ./app_entrypoint.sh && chmod +x ./test_entrypoint.sh
