# knope
knope is a microservice that generates PDFs from a template using [Handlebars](https://github.com/wycats/handlebars.js), [Markdown](https://github.com/Python-Markdown/markdown), and HTML.

## Usage
Make a `POST` request to the service with a `template` and `context`. For example:
```
Command to run docker
curl with {template: "<html><head><style>body {text-align: center;}</style></head><body><h1>City Charter</h1><p>**{{city}}, {{state}}**</p></body></html>", context: {city: "Pawnee", state: "Indiana"}} 
```

## Environmental Variables

Optionally, set a `AUTH_TOKEN` environment variable in knope, and it will be required as `token` in the request payload.

Listens to the `PORT` environmental variable when running in production (with Nginx and uWSGI).

## Note on wkhtmltopdf

`pdfkit` depends on `wkhtmltopdf`. Installing it seems like it would be as simple as `sudo apt-get install wkhtmltopdf`, but that version don't support all features we might want, like page footers. [Thanks to yajra](https://gist.github.com/yajra/80ae402e2084191cd1f6e17fa581320e) for the method of installing wkhtmltopdf with patched qt.
