FROM python:3.11-slim

RUN apt-get update -qq && apt-get install -y locales

RUN echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
  locale-gen ru_RU.UTF-8 && \
  /usr/sbin/update-locale LANG=ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

WORKDIR /blog

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
