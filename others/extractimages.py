import fitz  # PyMuPDF
import os

def extract_images(pdf_path, output_folder="images"):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    img_count = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            img_filename = f"page{page_index+1}_img{img_index+1}.{image_ext}"
            img_path = os.path.join(output_folder, img_filename)

            with open(img_path, "wb") as f:
                f.write(image_bytes)

            img_count += 1

    print(f"✅ Extracted {img_count} images to '{output_folder}'")

# Usage
extract_images("input.pdf")