FROM amd64/python:latest

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["uvicorn", "api.app:app", "--port", "5000", "--host", "0.0.0.0"]
