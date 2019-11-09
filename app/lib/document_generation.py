import pdfkit
import markdown
from pybars import Compiler

def save_pdf(template, content, options, file_path):
	html_content = markdown_to_html(template, content)

	pdfkit.from_string(
		html_content,
		file_path,
		options=options
	)

def markdown_to_html(template, content):
	compiler = Compiler()
	markdown_with_content = compiler.compile(template)(content)
	md = markdown.Markdown(extensions=["extra"])
	return md.convert(markdown_with_content)

DEFAULT_PDF_OPTIONS = {
	"margin-top": "0.75in",
	"margin-right": "0.75in",
	"margin-bottom": "0.75in",
	"margin-left": "0.75in"
}
