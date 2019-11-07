import os, time, random, glob

import pdfkit
import markdown
from pybars import Compiler

from flask import Flask, send_file, send_file, request

app = Flask(__name__)

app_auth_token = os.getenv("AUTH_TOKEN")

@app.route("/")
def hello():
    return send_file("static/index.html")

@app.route("/generate", methods=["GET", "POST"])
def generate():
	delete_old_temp_files()

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

		temp_file_path = get_temp_file_path(ext="pdf")

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

TEMP_DIR = "./tmp/"
def ensure_temp_directory_exists():
	if not os.path.exists(TEMP_DIR):
	    os.makedirs(TEMP_DIR)

SECONDS_TILL_DELETION = 30

def delete_old_temp_files():
	now = int(time.time())
	for filepath in glob.glob("%s/*" % TEMP_DIR):
		filename = os.path.basename(filepath)
		try:
			timepart = int(filename.split("-")[0])
			if (timepart + SECONDS_TILL_DELETION) < now:
				os.remove(filepath)

		except ValueError:
			pass

def get_temp_file_path(ext="txt"):
	now = int(time.time())
	filename = "%i-%i.%s" % (now, random.randint(0, 10000000), ext)
	return "%s/%s" % (TEMP_DIR, filename)

ensure_temp_directory_exists()
delete_old_temp_files()

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

if __name__ == "__main__":
	# For development
	app.run(host="0.0.0.0", debug=True, port=5000)
