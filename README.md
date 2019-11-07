# knope
knope is a microservice that generates PDFs from a template using [Handlebars](https://github.com/wycats/handlebars.js), [Markdown](https://github.com/Python-Markdown/markdown), and HTML.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)]([![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/mainvest/knope)

## Usage
Make a `POST` request to the service with a `template` and `context`. For example:
```
Command to run docker
curl with {template: "<html><head><style>body {text-align: center;}</style></head><body><h1>City Charter</h1><p>**{{city}}, {{state}}**</p></body></html>", context: {city: "Pawnee", state: "Indiana"}} 
```

Optionally, set a `token` environment variable in knope, and it will be required as `token` in the request payload.
