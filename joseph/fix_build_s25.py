import re

# Read the original build_s21.py
with open('/Users/macbook/GitHub/biblia-estudo/joseph/build_s21.py', 'r') as f:
    content = f.read()

# Replace N = 21 with N = 25
content = re.sub(r'N = 21', 'N = 25', content)

# Replace the pdf path comment and the actual string? Actually the string uses f-string, so we only need to change the comment if we want, but the f-string uses N+1, so it will be sessao-26.pdf when N=25.
# We'll leave the f-string as is, but update the comment for clarity.
content = re.sub(r'sessao-\{N\+1\}\.pdf  # sessao-22\.pdf', 'sessao-{N+1}.pdf  # sessao-26.pdf', content)

# Update localStorage keys
content = re.sub(r"localStorage\.setItem\('joseph-s2-lang',l\)", "localStorage.setItem('joseph-s25-lang',l)", content)
content = re.sub(r"localStorage\.getItem\('joseph-s2-lang'\)", "localStorage.getItem('joseph-s25-lang')", content)

# Write the new file
with open('/Users/macbook/GitHub/biblia-estudo/joseph/build_s25.py', 'w') as f:
    f.write(content)

print("File written.")