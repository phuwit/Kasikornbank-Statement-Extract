import sys
import pypdfium2 as pdfium

def main() -> None:
    filename = sys.argv[1]
    password = sys.argv[2]

    # pdf = pdfium.PdfDocument(input=filepath)
    pdf = pdfium.PdfDocument(input=filename, password=password)

    filecontents = ""
    for page in pdf:
        textpage = page.get_textpage()
        width, height = page.get_size()
        text = textpage.get_text_bounded(left=67, bottom=98, right=width-60.5, top=height-194)
        filecontents += text

    with open(f'{filename}.txt', mode="wt") as file:
        file.write(filecontents)


if __name__ == "__main__":
    main()
