from html.parser import HTMLParser

path = "exodus-overview/modulo-3/sessao-16.html"
with open(path) as f:
    html = f.read()

class V(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void = {"meta","link","br","hr","img","input","area","base","col","embed","source","track","wbr"}
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.stack:
            self.errors.append(f"extra </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            # pop until match
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed <{self.stack[-1]}> before </{tag}>")
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}>")

p = V()
p.feed(html)
print("unclosed at end:", p.stack)
print("errors:", p.errors)

# Count body paragraphs and bullets present
import re
bodies = re.findall(r'<p class="body reveal">', html)
bullets = re.findall(r'<ul class="bullets reveal">', html)
li = re.findall(r'<li>', html)
print("p.body:", len(bodies), "ul.bullets:", len(bullets), "li:", len(li))
print("div count:", html.count("<div"), "close:", html.count("</div>"))
