import sys
import pypdfium2 as pdfium

def main() -> None:
    filename = sys.argv[1]
    password = sys.argv[2]

    # pdf = pdfium.PdfDocument(input=filepath)
    pdf = pdfium.PdfDocument(input=filename, password=password)

    filecontents = ""
    for page in pdf:
        # bitmap = page.render(
        #     scale = 1,    # 72dpi resolution
        #     rotation = 0, # no additional rotation
        #     crop=(67, 98, 60.5, 193.5)
        # )
        # pil_image = bitmap.to_pil()
        # pil_image.show()

        textpage = page.get_textpage()
        width, height = page.get_size()
        # width, height = page.get_bbox()
        # print(page.get_bbox())
        text = textpage.get_text_bounded(left=67, bottom=98, right=width-60.5, top=height-194)
        # print(text)
        filecontents += text

    with open(f'{filename}.txt', mode="wt") as file:
        file.write(filecontents)

    # text = "\n".join(
    #     p.get_textpage().get_text_range()
    #     for p in pdfium.PdfDocument(pdf)
    # )


if __name__ == "__main__":
    main()
