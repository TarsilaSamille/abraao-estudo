#!/usr/bin/env python3
"""Audit verbatim fidelity of sessao-N.html vs teacher-notes PDF.
For each course with a *teacher-notes.pdf, find each 'Session N:' content block
(start = first page >4 containing 'Session N:' AND 'Key Takeaways'; end = page before next 'Session N+1:').
Compute EN word coverage: PDF words (len>=4) found in HTML lang-en spans (or stripped HTML if small).
Report coverage% per session; flag < 85%.
"""
import subprocess, re, os, glob, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def pdf_pages(pdf):
    out = subprocess.run(['pdftotext','-layout',pdf,'-'], capture_output=True, text=True).stdout
    return out.split('\f')

def session_ranges(pages):
    """Return dict N -> (start_page, end_page) using content markers (not TOC)."""
    n = len(pages)
    # find all content session starts: page>4 with 'Session N:' and 'Key Takeaways'
    starts = {}
    for i, p in enumerate(pages, 1):
        if i <= 4:
            continue
        m = re.search(r'Session\s+(\d+)\s*:', p)
        if m and 'Key Takeaways' in p:
            starts[int(m.group(1))] = i
    # also catch sessions without 'Key Takeaways' in first page (fallback: 'Session N:' with substantial prose)
    for i, p in enumerate(pages, 1):
        if i <= 4:
            continue
        m = re.search(r'Session\s+(\d+)\s*:', p)
        if m and int(m.group(1)) not in starts:
            starts.setdefault(int(m.group(1)), i)
    nums = sorted(starts)
    ranges = {}
    for idx, nn in enumerate(nums):
        s = starts[nn]
        e = n
        if idx + 1 < len(nums):
            nxt = nums[idx+1]
            # next start page; our end is the page before it (unless gap already known)
            e = starts[nxt] - 1
        ranges[nn] = (s, e)
    return ranges

def en_words(html):
    spans = re.findall(r'lang-en">([^<]+)</span>', html)
    en = ' '.join(spans)
    if len(en) < 2000:
        en = re.sub(r'<[^>]+>', ' ', html)
    return set(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", en))

def main():
    results = {}
    courses = [d for d in os.listdir(REPO) if os.path.isdir(os.path.join(REPO,d))]
    for course in sorted(courses):
        pdfs = glob.glob(os.path.join(REPO, course, '*teacher-notes.pdf'))
        if not pdfs:
            continue
        pdf = pdfs[0]
        pages = pdf_pages(pdf)
        ranges = session_ranges(pages)
        course_res = {}
        for nn in sorted(ranges):
            s, e = ranges[nn]
            # extract pdf text for range
            txt = subprocess.run(['pdftotext','-f',str(s),'-l',str(e),pdf,'-'], capture_output=True, text=True).stdout
            txt = re.sub(r'Class Notes.*?\d+ of \d+', '', txt)
            txt = re.sub(r'\n\d+\n', ' ', txt)
            exp = set(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", txt))
            html_path = None
            for pat in (f'sessao-{nn}.html',):
                cand = None
                for mod in ['modulo-1','modulo-2','modulo-3','modulo-4','modulo-5','modulo-6','modulo-7','modulo-8']:
                    c = os.path.join(REPO, course, mod, pat)
                    if os.path.exists(c):
                        cand = c; break
                if cand is None:
                    hits = glob.glob(os.path.join(REPO, course, '**', pat), recursive=True)
                    if hits:
                        cand = hits[0]
                if cand:
                    html_path = cand; break
            if not html_path:
                course_res[nn] = {'cov': None, 'status': 'NO_HTML', 'pages': [s,e]}
                continue
            h = open(html_path, encoding='utf-8').read()
            got = en_words(h)
            cov = round(100*len(exp & got)/max(1,len(exp)), 1)
            status = 'OK' if cov >= 85 else 'LOW'
            course_res[nn] = {'cov': cov, 'status': status, 'pages': [s,e], 'file': os.path.relpath(html_path, REPO)}
        results[course] = course_res
    # print summary
    print("=== VERBATIM COVERAGE AUDIT ===")
    low = []
    for course in sorted(results):
        for nn in sorted(results[course], key=lambda x:int(x)):
            r = results[course][nn]
            cov = r['cov']; st = r['status']
            if st == 'NO_HTML':
                print(f"  [NO_HTML] {course} S{nn} (pdf pág {r['pages']})")
                low.append((course, nn, r))
            else:
                flag = '' if st=='OK' else '  <-- CHECK'
                print(f"  {course}/S{nn:>2} cov={cov:5}% {st} ({r['file']}, pdf {r['pages']}){flag}")
                if st=='LOW':
                    low.append((course, nn, r))
    print(f"\nTotal cursos: {len(results)}  | Sessões com baixa cobertura: {len(low)}")
    with open(os.path.join(REPO,'bots','state','audit_verbatim.json'),'w') as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("Escrito bots/state/audit_verbatim.json")

if __name__ == '__main__':
    main()
