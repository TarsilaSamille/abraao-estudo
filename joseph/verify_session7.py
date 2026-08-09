import os
import re

base = os.getcwd()
N = 7
# We expect the file in modulo-2 because session 7 is in the 5-9 range
output_dir = os.path.join(base, "modulo-2")
output_path = os.path.join(output_dir, f"sessao-{N}.html")
img_dir = os.path.join(output_dir, f"img/sessao-{N}")

print(f"Checking {output_path}")
if not os.path.exists(output_path):
    print("ERROR: Output file does not exist")
    exit(1)

with open(output_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check title
title_match = re.search(r'<title>(.*?)</title>', content)
if not title_match:
    print("ERROR: Title tag not found")
    exit(1)
title = title_match.group(1)
expected_title_pt = f"Sessão {N}: Descendo para o Poço"
if title != expected_title_pt:
    print(f"ERROR: Title mismatch. Expected: {expected_title_pt}, Got: {title}")
    exit(1)
print(f"Title OK: {title}")

# Check localStorage key
if "localStorage.setItem('joseph-s7-lang',l)" not in content:
    print("ERROR: localStorage key for joseph-s7-lang not found")
    exit(1)
if "localStorage.getItem('joseph-s7-lang')" not in content:
    print("ERROR: localStorage get for joseph-s7-lang not found")
    exit(1)
print("localStorage key updated OK")

# Check that the old key is not present (optional)
if "localStorage.setItem('joseph-s2-lang',l)" in content:
    print("WARNING: Old localStorage key for joseph-s2-lang still present")
if "localStorage.getItem('joseph-s2-lang')" in content:
    print("WARNING: Old localStorage get for joseph-s2-lang still present")

# Check for image tags (we expect 4 images)
img_tags = re.findall(r'<img src="([^"]+)"', content)
expected_imgs = [f"img/sessao-{N}/p{i+1}-vector.png" for i in range(4)]
for img in expected_imgs:
    if img not in img_tags:
        print(f"ERROR: Expected image tag for {img} not found")
        exit(1)
print(f"Image tags OK: Found {len(img_tags)} images, expected 4")

# Check that the images directory exists and files are there
if not os.path.isdir(img_dir):
    print(f"ERROR: Image directory {img_dir} does not exist")
    exit(1)
for i in range(4):
    img_path = os.path.join(img_dir, f"p{i+1}-vector.png")
    if not os.path.exists(img_path):
        print(f"ERROR: Image file {img_path} does not exist")
        exit(1)
print("Image files exist OK")

print("All checks passed.")