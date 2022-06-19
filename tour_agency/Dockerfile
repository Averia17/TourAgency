FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
RUN apt-get update \
    && apt-get -y install curl \
    && apt-get install libgdal-dev -y
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]