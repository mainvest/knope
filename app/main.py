import os
import pdfkit
import markdown
from pybars import Compiler

from flask import Flask, send_from_directory, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Knope!"

@app.route("/generate")
def generate():
	template = request.args.get("template", "Default *content*!")
	dynamic_content = {}

	html_content = generate_html(template, dynamic_content)

	response_format = request.args.get("format", "pdf")

	if response_format == "pdf":
		pdf_options = DEFAULT_PDF_OPTIONS
		pdfkit.from_string(
			html_content,
			"./tmp/pdfs/test.pdf",
			options=pdf_options
		)

		return send_from_directory(TEMP_PDF_DIR, "test.pdf")

	elif response_format == "html":
		return html_content

	else:
		return "Unrecognized format: %s" % response_format, 400

DEFAULT_PDF_OPTIONS = {
	'margin-top': '0.75in',
	'margin-right': '0.75in',
	'margin-bottom': '0.75in',
	'margin-left': '0.75in',
	'footer-center': '[page]',
}

TEMP_PDF_DIR = "./tmp/pdfs/"
def ensure_temp_pdf_directory_exists():
	if not os.path.exists(TEMP_PDF_DIR):
	    os.makedirs(TEMP_PDF_DIR)
ensure_temp_pdf_directory_exists()

def generate_html(template, content):
	compiler = Compiler()
	markdown_with_content = compiler.compile(template)(content)
	md = markdown.Markdown(extensions=['extra'])
	return md.convert(markdown_with_content)


if __name__ == "__main__":
	# For development
	app.run(host='0.0.0.0', debug=True, port=5000)
