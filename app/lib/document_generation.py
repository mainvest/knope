from datetime import datetime
import base64

import pdfkit
import markdown
from pybars import Compiler
from dateutil.parser import parse as parsedate

def save_pdf(template, content, options, file_path):
	html_content = markdown_to_html(template, content)

	pdfkit.from_string(
		html_content,
		file_path,
		options=options
	)

def file_to_base64(file_path):
	data = open(file_path, "rb").read()
	return base64.b64encode(data)

def markdown_to_html(template, content):
	compiler = Compiler()
	live_template = compiler.compile(template)
	markdown_with_content = live_template(content, helpers=TEMPLATE_HELPERS)
	md = markdown.Markdown(extensions=["extra"])
	return md.convert(markdown_with_content)

def pluralize_helper(this, count=None, singular=None, plural=None):
	if count == 1:
		return singular
	else:
		return plural

def with_commas_helper(this, number=None):
	try:
		return '{:,}'.format(number)
	except (ValueError, TypeError):
		return None

def sum_helper(this, items=[], key=None):
	try:
		return sum(x.get(key, 0) for x in items)
	except (AttributeError, TypeError):
		return None

def datetime_helper(this, input_str=None, format="%Y-%m-%d"):
	try:
		return datetime.strftime(parsedate(input_str), format)
	except (ValueError, TypeError):
		return None

TEMPLATE_HELPERS = {
	"pluralize": pluralize_helper,
	"with_commas": with_commas_helper,
	"sum": sum_helper,
	"datetime": datetime_helper
}

DEFAULT_PDF_OPTIONS = {
	"margin-top": "0.75in",
	"margin-right": "0.75in",
	"margin-bottom": "0.75in",
	"margin-left": "0.75in"
}
