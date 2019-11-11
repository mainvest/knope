FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && \
	apt-get install --assume-yes libssl1.0-dev

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	mv wkhtmltox/bin/wkhtmlto* /usr/bin/ && \
	ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt

COPY ./app /app