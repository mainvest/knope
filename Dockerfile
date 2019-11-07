FROM tiangolo/uwsgi-nginx:python3.7

COPY ./app /app

RUN apt-get update && \
	apt-get install -y wkhtmltopdf && \
    pip install -r ./requirements.txt