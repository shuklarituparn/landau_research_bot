FROM python:3.9-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev gcc build-essential

RUN pip install -r./requirements.txt

CMD ["python", "main.py"]