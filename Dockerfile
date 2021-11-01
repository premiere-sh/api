FROM python:latest

WORKDIR /app

COPY . .

# RUN apt-get update && \
#   apt-get dist-upgrade -y && \
#   apt-get install -y mysql-apt-config mysql-shell && \ 
#   mysql_secure_installation

RUN pip install -r requirements.txt

CMD ["uvicorn", "api.app:app", "--port", "443", "--host", "0.0.0.0"]

