import re
import os

def create_session_file(module_dir, session_num, title, content):
    html_content = f"""<!doctype html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sessão {session_num}: {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-white font-sans text-slate-800">
    <div class="min-h-screen p-8">
        <div class="flex min-h-screen flex-col p-8 md:p-12">
            <main class="flex flex-1 flex-col items-center justify-center">
                <a href="index.html" class="mb-8 self-start text-sky-600 hover:underline">← Voltar para o Índice</a>
                
                <article class="prose prose-slate max-w-3xl lg:prose-xl">
                    <h1 class="text-4xl font-bold text-slate-900">Sessão {session_num}: {title}</h1>
                    <div class="mt-8 whitespace-pre-wrap text-lg leading-relaxed text-slate-700">
{content}
                    </div>
                </article>
            </main>
        </div>
    </div>
</body>

</html>"""
    
    filename = f"{module_dir}/sessao-{session_num}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created {filename}")

def main():
    with open("extracted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Split by Session headers
    # Regex to find "Session X: Title"
    # We use capturing group for the split to keep the delimiter
    pattern = r"(Session \d+: .+)"
    parts = re.split(pattern, text)
    
    current_session = None
    current_title = None
    current_content = []
    
    # Mapping sessions to modules
    session_to_module = {}
    for i in range(11, 16): session_to_module[i] = "modulo-3"
    for i in range(16, 20): session_to_module[i] = "modulo-4"
    for i in range(20, 25): session_to_module[i] = "modulo-5"
    for i in range(25, 31): session_to_module[i] = "modulo-6"

    for part in parts:
        if part.startswith("Session "):
            # If we have a previous session, save it
            if current_session and current_session in session_to_module:
                module_dir = session_to_module[current_session]
                content_str = "".join(current_content).strip()
                create_session_file(module_dir, current_session, current_title, content_str)
            
            # Start new session
            match = re.match(r"Session (\d+): (.+)", part)
            if match:
                current_session = int(match.group(1))
                current_title = match.group(2).strip()
                current_content = []
        else:
            if current_session:
                current_content.append(part)

    # Save the last session
    if current_session and current_session in session_to_module:
        module_dir = session_to_module[current_session]
        content_str = "".join(current_content).strip()
        create_session_file(module_dir, current_session, current_title, content_str)

if __name__ == "__main__":
    main()
