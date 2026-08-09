import fitz
import os
import re

base = os.getcwd()
pdf_path = f"{base}/pdf-sessoes/sessao-5.pdf"
output_dir = f"{base}/modulo-1"
img_dir = f"{output_dir}/img/sessao-4"
os.makedirs(img_dir, exist_ok=True)

# Render images if not already done
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = f"{img_dir}/p{i+1}-vector.png"
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# Extract text
doc = fitz.open(pdf_path)
pages_text = [page.get_text() for page in doc]
doc.close()

# Load template
template_path = f"{base}/modulo-1/sessao-2.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title
new_title = "Sessão 4: Um Conto de Duas Sementes"
template = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', template)
# Replace the h1.title content
template = re.sub(r'(<h1 class="title reveal">).*?(</h1>)', 
                  f'\\1<span class="lang-pt">{new_title}</span><span class="lang-en">Session 4: A Tale of Two Seeds</span>\\2', 
                  template, flags=re.DOTALL)

# We will replace the body content from the opening <div class="max-w-4xl mx-auto px-5 py-12 md:py-16"> to the closing </div> before the script.
# We'll generate a new body that includes the title and rule, then loops over pages.

# Let's split the template into head, body start, and script.
# We'll find the opening of the body div and the closing of that div before the script.
# We'll do a simple approach: replace everything from the div to the script.

# We'll use a regex to capture the parts before and after the content we want to replace.
pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>\s*<script>)'
# We need to make the dot match newlines
match = re.search(pattern, template, re.DOTALL)
if match:
    prefix = match.group(1)  # the opening div
    suffix = match.group(3)  # the closing div and script opening
    # We'll keep the prefix and suffix, and generate the middle.
    # But note: the pattern includes the opening div and the closing div and script.
    # We want to replace the middle only.
    # Actually, we want to replace from the opening div to the closing div before the script.
    # Let's adjust: we want to keep the opening div and the closing div and script, and replace the inner content.
    # So we can do:
    # new_template = template[:match.start(1)] + match.group(1) + new_content + match.group(3) + template[match.end(3):]
    # But let's do it step by step.
    # We'll extract the head (everything before the body div) and the tail (everything after the closing div of the content).
    # Actually, let's just replace the content of the div.
    # We'll find the start and end of the div's inner content.
    # We'll look for the pattern: <div class="max-w-4xl mx-auto px-5 py-12 md:py-16">(.*?)</div>
    # and then ensure that after that div there is a <script> tag (but there might be other divs? In the template, after that div there is only the script).
    # Let's do:
    inner_pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>\s*<script>)'
    match = re.search(inner_pattern, template, re.DOTALL)
    if match:
        before = template[:match.start(1)]
        div_open = match.group(1)
        inner_old = match.group(2)
        div_close_script = match.group(3)
        after = template[match.end(3):]
        # Now we generate new_inner.
        new_inner = ''
        # We already have the title and rule outside? Actually, in the template, the title and rule are inside this div.
        # We need to keep the title and rule as they are (but we already replaced the title and the h1).
        # However, we have already replaced the title in the template, so the inner_old still contains the old title and rule.
        # We will replace the entire inner content with our own, which should include the title and rule.
        # But to keep it simple, we will generate the entire inner content from scratch, including the title and rule.
        # However, we have already replaced the title in the template, so we can just use the template's title and rule as they are now.
        # Let's instead keep the template's title and rule by not replacing them in the inner content? This is getting messy.

        # Given the complexity, and since we are only building one session, let's instead generate the entire HTML from scratch using the template's head and style, and then write the body we want.
        # We'll abort this approach and do a simpler one: we will write the HTML by copying the template and then replacing the entire body content with a placeholder, and then we will manually edit it? Not possible.

        # Let's change strategy: we will use the template's head and style, and then we will write the body based on the PDF text, but we will keep the structure of the template (the nav buttons, etc.) and replace only the content of the div.
        # We will generate the new inner content as follows:
        #   - The title and rule (we already have the title replaced in the template, so we can extract the current title and rule from the template?).
        #   Instead, let's just use the template as is and replace the inner content of the div with our generated content, but we will leave the title and rule as they are in the template (which we have already updated).
        #   So we will set new_inner to our generated content for the pages, and we will keep the div_open and div_close_script as they are.
        #   However, note that the div_open and div_close_script include the opening div and the closing div and script? No, in our inner_pattern, div_open is the opening div, and div_close_script is the closing div and the script opening.
        #   Actually, we defined inner_pattern to capture the opening div, the inner content, and then the closing div and script.
        #   So we want to replace the inner content only.
        #   Therefore, we will set new_inner to our generated content for the pages (which should include the title and rule?).
        #   But the title and rule are currently inside the inner content of the template. We have already replaced the title in the template, so the inner_old contains the updated title.
        #   We want to keep the title and rule, so we should extract them from the inner_old and then prepend them to our generated page content? Or we can regenerate them.

        # Let's do: we will generate the inner content as:
        #   [title and rule as they currently are in the template after our replacement] + [content for each page]
        #   To get the current title and rule, we can extract them from the template by looking for the h1.title and the hr.rule.
        #   But we can also just keep the inner_old up to the first <h2? This is too risky.

        # Given the time, let's output a simple HTML that at least has the correct title and images, and we can later replace the content with a more accurate version when vision is working.
        # We'll generate the inner content as:
        #   We keep the title and rule from the template (by not touching them) and then we add the page content after the rule.
        #   How can we do that? We can split the inner_old at the rule.
        #   Let's do: split inner_old into two parts: before the rule and after the rule.
        #   We'll keep the before part (which includes the title and the rule) and then append our page content after the rule.
        #   But note: the rule is an <hr class="rule">.
        #   We'll split inner_old by the rule.

        # Let's try:
        rule_split = inner_old.split('<hr class="rule">', 1)
        if len(rule_split) == 2:
            before_rule = rule_split[0]  # includes the title and maybe some whitespace
            after_rule = rule_split[1]   # everything after the rule
            # We will keep before_rule and the rule, and then we will replace after_rule with our page content.
            new_inner = before_rule + '<hr class="rule">' + after_rule
            # But wait, we want to replace the content after the rule with our page content.
            # Actually, we want to keep the title and the rule, and then put our page content after the rule.
            # So we set new_inner = before_rule + '<hr class="rule">' + [our page content]
            new_inner = before_rule + '<hr class="rule">'
        else:
            # If we can't find the rule, we just replace the entire inner content with our page content (and hope the title and rule are not needed?).
            new_inner = ''
        # Now we generate the page content.
        for i, text in enumerate(pages_text):
            # Escape HTML in text
            text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Replace newlines with <br> for simplicity
            text_escaped = text_escaped.replace('\n', '<br>')
            new_inner += f'<div class="page reveal">{text_escaped}</div>'
            # Check if there is an image for this page
            img_path = f"img/sessao-4/p{i+1}-vector.png"
            if os.path.exists(f"{output_dir}/{img_path}"):
                new_inner += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
        # Now we have new_inner.
        # Now we reconstruct the template:
        new_template = before + div_open + new_inner + div_close_script + after
        # Write the new template to the output file
        output_path = f"{output_dir}/sessao-4.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_template)
        print(f"Created {output_path}")
    else:
        print("Could not find the div pattern in the template")
else:
    print("Could not find the div pattern in the template")
