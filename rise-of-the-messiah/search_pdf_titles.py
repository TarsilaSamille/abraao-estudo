from pypdf import PdfReader

reader = PdfReader("rise-of-the-messiah-teacher-notes.pdf")
titles = [
    "Jesus, Isaiah, and Immanuel",
    "Magi and Herod",
    "Out of Egypt",
    "The Nazarene",
    "John the Baptist",
    "The Baptism of Jesus",
    "Jesus Tested in the Wilderness",
    "Jesus Passes the Test",
    "Jesus' Kingdom Mission",
    "Reflecting on Matthew 1-4"
]

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    for title in titles:
        if title in text:
            print(f"--- Found '{title}' on Page {i+1} ---")
            print(text)
            print("\n" + "="*50 + "\n")
