FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	mv wkhtmltox/bin/wkhtmlto* /usr/bin/ && \
	ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

RUN pip install -r ./requirements.txt

# This image uses the LISTEN_PORT by default
# We need to listen on PORT for heroku.
# `entrypoint.sh` seems to be the key, but I'm editing the other one
# for neatness (and because I'm not sure when it is used)
RUN sed -i 's/LISTEN_PORT/PORT/g' /uwsgi-nginx-entrypoint.sh
RUN sed -i 's/LISTEN_PORT/PORT/g' /entrypoint.sh