FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install flask telebot requests psutil --quiet

COPY . .

CMD ["python", "drx.py"]