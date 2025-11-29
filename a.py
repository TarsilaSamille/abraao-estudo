import fitz  # PyMuPDF

#  doc = fitz.open("abraao/abraham-teacher-notes.pdf")
doc = fitz.open("messiah/rise-of-the-messiah-teacher-notes.pdf")
for i, page in enumerate(doc):
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n < 5:        # RGB or grayscale
            pix.save(f"image_{i}_{xref}.png")
        else:                # CMYK
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.save(f"image_{i}_{xref}.png")
            pix1 = None
        pix = None
