FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p media
RUN python3 manage.py makemigrations && python3 manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
