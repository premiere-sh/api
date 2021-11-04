FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "api.app:app", "--port", "5000", "--host", "0.0.0.0"]

