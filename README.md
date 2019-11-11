# knope
knope is a microservice that generates PDFs from a template using [Handlebars](https://github.com/wycats/handlebars.js), [Markdown](https://github.com/Python-Markdown/markdown), and HTML.

## Usage
Make a `POST` request to `/generate` with a `template` and `context` parameter.

Development:
```
docker-compose build
docker-compose up
curl -X POST -H "Content-Type: application/json" \
 -d '{"template":"<html><head><style>body {text-align: center;}</style></head><body><h1>City Charter</h1><p>**{{city}}, {{state}}**</p></body></html>","context":{"city": "Pawnee", "state": "Indiana"}}' \
 http://0.0.0.0:5000/generate -o output.pdf
```

Production:
```
docker run -d --name knope -p 80:80 -e AUTH_TOKEN=SET_YOUR_TOKEN_HERE mainvest/knope
```

### Authentication

Optionally, set an `AUTH_TOKEN` environment variable in knope, and it will be required as `token` in the request payload.

### Format

Pass `format=html` to retrieve the HTML output of the Handlebars processing, prior to PDF creation.

## Dependencies

`pdfkit` depends on `wkhtmltopdf`, but to enable some features, including page footers, we need to rely on [this method](https://gist.github.com/yajra/80ae402e2084191cd1f6e17fa581320e) for installation.
# knope
knope is a microservice that generates PDFs from a template using [Handlebars](https://github.com/wycats/handlebars.js), [Markdown](https://github.com/Python-Markdown/markdown), and HTML.

## Usage
Make a `POST` request to the service with a `template` and `context`. For example:
```
Command to run docker
curl with {template: "<html><head><style>body {text-align: center;}</style></head><body><h1>City Charter</h1><p>**{{city}}, {{state}}**</p></body></html>", context: {city: "Pawnee", state: "Indiana"}}
```

## Environmental Variables

Set a `AUTH_TOKEN` environment variable in knope, and it will be required as `token` in the request payload. Otherwise, there's no authentication.

## docker-compose for dev

To run in development on port 5000:
```
docker-compose build
docker-compose up
```

## Note on wkhtmltopdf

`pdfkit` depends on `wkhtmltopdf`. Installing it seems like it would be as simple as `sudo apt-get install wkhtmltopdf`, but that version don't support all features we might want, like page footers. [Thanks to yajra](https://gist.github.com/yajra/80ae402e2084191cd1f6e17fa581320e) for the method of installing wkhtmltopdf with patched qt.
