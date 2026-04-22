import fitz  # PyMuPDF
import os

def extract_embedded_images(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    img_count = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Using xref in name to avoid duplicates
            img_filename = f"img_{page_index}_{img_index}_{xref}.{image_ext}"
            img_path = os.path.join(output_folder, img_filename)

            with open(img_path, "wb") as f:
                f.write(image_bytes)
            img_count += 1

    print(f"✅ Extracted {img_count} embedded images to '{output_folder}'")

if __name__ == "__main__":
    pdf = "others/noah-to-abraham-teacher-notes.pdf"
    output = "others/noah-embedded-images"
    extract_embedded_images(pdf, output)
