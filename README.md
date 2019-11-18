# knope
knope is a microservice that generates PDFs from a template using Handlebars and Markdown with HTML.

## Usage
Make a `POST` request to `/generate` with a `template` and `context` parameter.

**Development**
```
docker-compose build
docker-compose up
curl -X POST -H "Content-Type: application/json" \
 -d '{"template":"<html><head><style>body {text-align: center;}</style></head><body><h1>City Charter</h1><p>**{{city}}, {{state}}**</p></body></html>","context":{"city": "Pawnee", "state": "Indiana"}}' \
 http://0.0.0.0:5000/generate -o output.pdf
```

**Production**
```
docker run -d --name knope -p 80:80 -e AUTH_TOKEN=SET_YOUR_TOKEN_HERE mainvest/knope
```

### Handlerbar Helpers

We have implemented a handful of custom handlebar helpers to help with document generation.

- pluralize: `{{pluralize count "cat" "cats"}}`
- with_commas: `{{with_commas 10202}}`
- sum: `{{sum items "value"}}`
- datetime: `{{sum date "%m/%d/%Y"}}` (uses python strftime formatting)

### Authentication

Optionally, set an `AUTH_TOKEN` environment variable in knope and it will be required as `token` in the request payload.

### Format

Include `{"format": "html"}` in the request to view the output from Handlebars as HTML.

## Dependencies

`pdfkit` depends on `wkhtmltopdf`, but to enable some features (such as page footers) we need to rely on [this method](https://gist.github.com/yajra/80ae402e2084191cd1f6e17fa581320e) for installation.
