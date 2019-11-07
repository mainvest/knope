import os

import pdfkit
import markdown
from pybars import Compiler

from flask import Flask, send_file, send_file, request

from lib import temp_files

app = Flask(__name__)

app_auth_token = os.getenv("AUTH_TOKEN")

@app.route("/")
def hello():
    return send_file("static/index.html")

@app.route("/generate", methods=["GET", "POST"])
def generate():
	temp_files.delete_expired_temp_files()

	params = merged_params()

	print((params["token"], app_auth_token), flush=True)

	if app_auth_token:
		if "token" not in params:
			return "Provide 'token' for authentication", 401
		elif params["token"] != app_auth_token:
			return "Invalid authentication token", 403

	template = params.get("template", "This is the *default* content!")
	dynamic_content = params.get("content", {})

	html_content = generate_html(template, dynamic_content)

	response_format = params.get("format", "pdf")

	if response_format == "pdf":
		pdf_options = DEFAULT_PDF_OPTIONS

		temp_file_path = temp_files.get_file_path(ext="pdf")

		pdfkit.from_string(
			html_content,
			temp_file_path,
			options=pdf_options
		)

		return send_file(temp_file_path)

	elif response_format == "html":
		return html_content

	else:
		return "Unrecognized format: %s" % response_format, 400

DEFAULT_PDF_OPTIONS = {
	"margin-top": "0.75in",
	"margin-right": "0.75in",
	"margin-bottom": "0.75in",
	"margin-left": "0.75in",
	"footer-center": "[page]",
}

def generate_html(template, content):
	compiler = Compiler()
	markdown_with_content = compiler.compile(template)(content)
	md = markdown.Markdown(extensions=["extra"])
	return md.convert(markdown_with_content)

def merged_params():
	all_params = {}
	all_params.update(request.args.to_dict())
	all_params.update(request.form.to_dict())
	json_data = request.get_json()
	if json_data:
		all_params.update(json_data)
	return all_params

temp_files.ensure_temp_directory_exists()
temp_files.delete_expired_temp_files()

if __name__ == "__main__":
	# For development
	app.run(host="0.0.0.0", debug=True, port=5000)
