FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
	mv wkhtmltox/bin/wkhtmlto* /usr/bin/ && \
	ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

RUN pip install -r ./requirements.txt