from weasyprint import HTML
html_input='register.html'
pdf_output='output.pdf'
HTML(html_input).write_pdf(pdf_output)
