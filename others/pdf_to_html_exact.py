import fitz
import os
import sys

def pdf_to_html_exact(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    img_dir = os.path.join(output_dir, "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    doc = fitz.open(pdf_path)
    html_content = ["""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PDF to HTML - Exact</title>
    <style>
        body {
            background-color: #525659;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .controls {
            position: fixed;
            top: 10px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
        }
        .page {
            background-color: white;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            flex-shrink: 0;
        }
        .text-span {
            position: absolute;
            white-space: pre;
            line-height: 1;
            transform-origin: 0 0;
        }
        .image {
            position: absolute;
        }
        @media print {
            body { background: white; padding: 0; }
            .controls { display: none; }
            .page { margin: 0; box-shadow: none; page-break-after: always; }
        }
    </style>
</head>
<body>
    <div class="controls">
        Total Pages: """ + str(len(doc)) + """
    </div>
"""]

    for page_num in range(len(doc)):
        page = doc[page_num]
        width = page.rect.width
        height = page.rect.height
        
        html_content.append(f'    <div class="page" style="width: {width}px; height: {height}px;" id="page-{page_num+1}">')
        
        # Get blocks
        blocks = page.get_text("dict")["blocks"]
        
        image_count = 0
        for block in blocks:
            if block["type"] == 0:  # Text
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        bbox = span["bbox"]
                        font_size = span["size"]
                        font_family = span["font"]
                        flags = span["flags"]
                        
                        # Flags: bit 0: superscript, 1: italic, 2: serifed, 3: monospaced, 4: bold
                        is_italic = flags & 2
                        is_bold = flags & 16
                        
                        c = span.get("color", 0)
                        r = (c >> 16) & 255
                        g = (c >> 8) & 255
                        b = c & 255
                        color_hex = f"#{r:02x}{g:02x}{b:02x}"

                        style_parts = [
                            f"left: {bbox[0]}px",
                            f"top: {bbox[1]}px",
                            f"font-size: {font_size}px",
                            f"color: {color_hex}",
                            f"font-family: '{font_family}', sans-serif"
                        ]
                        
                        if is_bold: style_parts.append("font-weight: bold")
                        if is_italic: style_parts.append("font-style: italic")
                        
                        style = "; ".join(style_parts)
                        html_content.append(f'        <span class="text-span" style="{style}">{text}</span>')
            
            elif block["type"] == 1:  # Image
                bbox = block["bbox"]
                img_ext = block.get("ext", "png")
                img_bytes = block.get("image")
                if not img_bytes:
                    continue
                    
                img_filename = f"page_{page_num+1}_img_{image_count}.{img_ext}"
                img_path = os.path.join(img_dir, img_filename)
                
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                
                style = (
                    f"left: {bbox[0]}px; "
                    f"top: {bbox[1]}px; "
                    f"width: {bbox[2] - bbox[0]}px; "
                    f"height: {bbox[3] - bbox[1]}px;"
                )
                html_content.append(f'        <img class="image" src="images/{img_filename}" style="{style}">')
                image_count += 1

        html_content.append('    </div>')
        if (page_num + 1) % 10 == 0 or (page_num + 1) == len(doc):
            print(f"Processed page {page_num+1}/{len(doc)}")

    html_content.append("""
</body>
</html>
""")

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
    
    print(f"✅ HTML generated at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_html_exact.py <pdf_path> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_html"
    
    pdf_to_html_exact(pdf_path, output_dir)
