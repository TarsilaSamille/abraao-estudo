from pypdf import PdfReader

reader = PdfReader("abraham-teacher-notes.pdf")

# Search for "Session 12" or "Sessão 12" or "Semente como Estrelas"
search_terms = ["Session 12", "Sessão 12", "Semente como Estrelas", "Seed Like Stars"]

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    for term in search_terms:
        if term in text:
            print(f"Found '{term}' on page {i} (PDF page {i+1})")
            print(f"Check image: pdf-images/page_{i}.png")
            print("-" * 50)
            break
