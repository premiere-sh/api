FROM python:latest

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["python", "-m", "uvicorn", "api.app:app", "--port", "5000", "--host", "0.0.0.0"]
