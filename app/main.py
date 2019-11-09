import os

from flask import Flask, send_file, send_file, request
from lib import temp_files, document_generation

app = Flask(__name__)

app_auth_token = os.getenv("AUTH_TOKEN")

@app.route("/")
def hello():
    return send_file("static/index.html")

@app.route("/generate", methods=["GET", "POST"])
def generate():
	# Deletes temporary files from past requests
	temp_files.delete_expired_temp_files()

	params = merged_params()

	# Checks for the `token` parameter to match AUTH_TOKEN from env
	auth_check = unauthorized_check(params)
	if auth_check:
		return auth_check

	# Template is a markdown template (which can include HTML)
	template = params.get("template", "This is the *default* Knope PDF!")

	# Data to be fed into the template using handlebars
	dynamic_content = params.get("content", {})

	# Valid options are PDF or HTML
	response_format = params.get("format", "pdf")

	if response_format == "pdf":
		# PDF options include:
		# - margin-top (+right, bottom, left)
		# - footer-center (+left, right)
		pdf_options = params.get("options", document_generation.DEFAULT_PDF_OPTIONS)

		# Save PDF to a temporary file and serves it for the request
		temp_file_path = temp_files.get_file_path(ext="pdf")
		document_generation.save_pdf(
			template, dynamic_content, pdf_options, temp_file_path
		)
		return send_file(temp_file_path)

	elif response_format == "html":
		# Makes the same subsitutions as the PDF method, but doesn't write to PDF
		return document_generation.markdown_to_html(template, dynamic_content)

	else:
		return "Unrecognized format: %s" % response_format, 400

def unauthorized_check(params):
	if app_auth_token:
		if "token" not in params:
			return "Provide 'token' for authentication", 401
		elif params["token"] != app_auth_token:
			return "Invalid authentication token", 403



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
