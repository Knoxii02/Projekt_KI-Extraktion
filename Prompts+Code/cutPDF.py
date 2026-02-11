from PyPDF2 import PdfReader, PdfWriter


INPUT_PDF = "DSOX1202A.pdf"
OUTPUT_PDF = f"DSOX1202A_cut.pdf"
PAGES = [5,6]


def cutPDF(pages):
	reader = PdfReader(INPUT_PDF)
	writer = PdfWriter()

	for page_number in pages:
		writer.add_page(reader.pages[page_number - 1])

	with open(OUTPUT_PDF, "wb") as output_file:
		writer.write(output_file)


if __name__ == "__main__":
	cutPDF(PAGES)
