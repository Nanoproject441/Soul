FROM python:3.9-slim

RUN pip install flask telebot requests psutil --quiet

CMD ["python", "drx.py"]