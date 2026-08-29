document.addEventListener("DOMContentLoaded", () => {
    const modal = document.createElement("div");
    modal.id = "verse-modal";
    modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/50 hidden";
    modal.innerHTML = `
        <div class="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
            <div class="mb-4 flex items-center justify-between">
                <h3 id="modal-title" class="text-xl font-bold text-slate-900"></h3>
                <button id="close-modal" class="text-slate-500 hover:text-slate-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div id="modal-content" class="max-h-[60vh] overflow-y-auto text-slate-700">
                <p>Carregando...</p>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    const modalTitle = modal.querySelector("#modal-title");
    const modalContent = modal.querySelector("#modal-content");
    const closeModal = modal.querySelector("#close-modal");

    function openModal() {
        modal.classList.remove("hidden");
    }

    function closeModalFunc() {
        modal.classList.add("hidden");
        modalContent.innerHTML = '<p>Carregando...</p>';
    }

    closeModal.addEventListener("click", closeModalFunc);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModalFunc();
    });

    function normalizeReference(reference){
        const cleaned = reference.replace(/\+/g, ' ');
        const m = cleaned.match(/^([^0-9]+)\s*(.*)$/);
        if (!m) return cleaned;
        let book = m[1].trim();
        const rest = m[2].trim();
        const map = {
            'Gênesis':'Genesis','Êxodo':'Exodus','Levítico':'Leviticus','Números':'Numbers','Deuteronômio':'Deuteronomy',
            'Josué':'Joshua','Juízes':'Judges','Rute':'Ruth','1 Samuel':'1 Samuel','2 Samuel':'2 Samuel','1 Reis':'1 Kings','2 Reis':'2 Kings',
            '1 Crônicas':'1 Chronicles','2 Crônicas':'2 Chronicles','Esdras':'Ezra','Neemias':'Nehemiah','Ester':'Esther','Jó':'Job',
            'Salmos':'Psalms','Provérbios':'Proverbs','Eclesiastes':'Ecclesiastes','Cantares':'Song of Songs','Isaías':'Isaiah','Jeremias':'Jeremiah',
            'Lamentações':'Lamentations','Ezequiel':'Ezekiel','Daniel':'Daniel','Oseias':'Hosea','Joel':'Joel','Amós':'Amos','Obadias':'Obadiah',
            'Jonas':'Jonah','Miqueias':'Micah','Naum':'Nahum','Habacuque':'Habakkuk','Sofonias':'Zephaniah','Ageu':'Haggai','Zacarias':'Zechariah',
            'Malaquias':'Malachi','Mateus':'Matthew','Marcos':'Mark','Lucas':'Luke','João':'John','Atos':'Acts','Romanos':'Romans',
            '1 Coríntios':'1 Corinthians','2 Coríntios':'2 Corinthians','Gálatas':'Galatians','Efésios':'Ephesians','Filipenses':'Philippians',
            'Colossenses':'Colossians','1 Tessalonicenses':'1 Thessalonians','2 Tessalonicenses':'2 Thessalonians','1 Timóteo':'1 Timothy',
            '2 Timóteo':'2 Timothy','Tito':'Titus','Filemom':'Philemon','Hebreus':'Hebrews','Tiago':'James','1 Pedro':'1 Peter','2 Pedro':'2 Peter',
            '1 João':'1 John','2 João':'2 John','3 João':'3 John','Judas':'Jude','Apocalipse':'Revelation'
        };
        // Handle common abbreviations
        const abbr = {'Gn':'Gênesis','Gn.':'Gênesis','Ex':'Êxodo','Ex.':'Êxodo'};
        if (abbr[book]) book = abbr[book];
        if (map[book]) book = map[book];
        return `${book} ${rest}`.trim();
    }

    function parseReferences(reference){
        const cleaned = reference.replace(/\+/g, ' ').trim();
        const m = cleaned.match(/^([^0-9]+)\s+(.+)$/);
        if (!m) return [normalizeReference(reference)];
        const bookPt = m[1].trim();
        const rest = m[2].trim();
        const normalizedBook = normalizeReference(`${bookPt} `).trim();
        // normalizedBook is like "Genesis" (without rest)
        const bookEn = normalizedBook;
        // Handle comma-separated verses, e.g., "10:5,32" or "16:1,6"
        const parts = rest.split(',').map(p=>p.trim()).filter(Boolean);
        let lastChapter = null;
        const refs = parts.map((p)=>{
            if (/^\d+:\d+(?:-\d+)?$/.test(p)){
                lastChapter = p.split(':')[0];
                return `${bookEn} ${p}`;
            }
            if (/^\d+$/.test(p) && lastChapter){
                return `${bookEn} ${lastChapter}:${p}`;
            }
            return `${bookEn} ${p}`;
        });
        return refs.length ? refs : [`${bookEn} ${rest}`];
    }

    // Split a cross-chapter range like "Genesis 20:1-22:19" into per-chapter queries.
    // Returns array of {book, chapter, fromVerse, toVerse} (toVerse null = whole chapter).
    function splitRange(book, rest) {
        const parts = rest.split(',').map(s => s.trim()).filter(Boolean);
        const out = [];
        let lastChapter = null;
        for (const p of parts) {
            const m = p.match(/^(\d+):(\d+)(?:\s*-\s*(\d+):(\d+))?$/);
            if (!m) {
                // fallback: single verse or bare, keep as-is
                out.push({ book, chapter: lastChapter, fromVerse: null, toVerse: null, raw: p });
                continue;
            }
            const ch = parseInt(m[1], 10);
            const v1 = parseInt(m[2], 10);
            if (m[3] !== undefined) {
                const ch2 = parseInt(m[3], 10);
                const v2 = parseInt(m[4], 10);
                if (ch === ch2) {
                    out.push({ book, chapter: ch, fromVerse: v1, toVerse: v2 });
                } else {
                    // cross-chapter: first chapter partial, middle full, last partial
                    out.push({ book, chapter: ch, fromVerse: v1, toVerse: null });
                    for (let c = ch + 1; c < ch2; c++) out.push({ book, chapter: c, fromVerse: null, toVerse: null });
                    out.push({ book, chapter: ch2, fromVerse: 1, toVerse: v2 });
                }
            } else {
                out.push({ book, chapter: ch, fromVerse: v1, toVerse: v1 });
            }
            lastChapter = ch;
        }
        return out;
    }

    function verseInRange(verse, q) {
        if (q.fromVerse === null) return true; // whole chapter
        return verse >= q.fromVerse && (q.toVerse === null || verse <= q.toVerse);
    }

    async function fetchChapter(book, chapter, attempt = 0) {
        const ref = `${book} ${chapter}`;
        const encoded = encodeURIComponent(ref).replace(/%3A/g, ':');
        const response = await fetch(`https://bible-api.com/${encoded}?translation=almeida`);
        if (!response.ok) {
            if (attempt < 2) { await new Promise(r => setTimeout(r, 400 * (attempt + 1))); return fetchChapter(book, chapter, attempt + 1); }
            throw new Error('HTTP ' + response.status);
        }
        return await response.json();
    }

    async function fetchVerse(reference) {
        openModal();
        const cleanedReference = reference.replace(/\+/g, ' ');
        modalTitle.textContent = cleanedReference;
        try {
            // If the reference has no book name (starts with a digit), default to Genesis
            // (used by inner diagram badges like "2:4-3:24" that inherit the book from a parent cluster)
            let ref = cleanedReference;
            if (/^\s*\d/.test(ref)) ref = 'Genesis ' + ref;
            // Strip trailing verse-letter suffixes the API doesn't understand (e.g. "7:17a", "11:10b-26a")
            ref = ref.replace(/([0-9])[a-z]\b/g, '$1');
            const m = ref.match(/^([^0-9]+?)\s*([\d:,.\\s-]+)$/);
            let book = ref, rest = '';
            if (m) { book = m[1].trim(); rest = m[2].trim(); }
            // Map PT book names to the English names the API expects
            const ptMap = {
                'Gênesis':'Genesis','Êxodo':'Exodus','Levítico':'Leviticus','Números':'Numbers','Deuteronômio':'Deuteronomy',
                'Josué':'Joshua','Juízes':'Judges','Rute':'Ruth','1 Samuel':'1 Samuel','2 Samuel':'2 Samuel','1 Reis':'1 Kings','2 Reis':'2 Kings',
                '1 Crônicas':'1 Chronicles','2 Crônicas':'2 Chronicles','Esdras':'Ezra','Neemias':'Nehemiah','Ester':'Esther','Jó':'Job',
                'Salmos':'Psalms','Provérbios':'Proverbs','Eclesiastes':'Ecclesiastes','Cantares':'Song of Songs','Isaías':'Isaiah','Jeremias':'Jeremiah',
                'Lamentações':'Lamentations','Ezequiel':'Ezekiel','Daniel':'Daniel','Oseias':'Hosea','Joel':'Joel','Amós':'Amos','Obadias':'Obadiah',
                'Jonas':'Jonah','Miqueias':'Micah','Naum':'Nahum','Habacuque':'Habakkuk','Sofonias':'Zephaniah','Ageu':'Haggai','Zacarias':'Zechariah',
                'Malaquias':'Malachi','Mateus':'Matthew','Marcos':'Mark','Lucas':'Luke','João':'John','Atos':'Acts','Romanos':'Romans',
                '1 Coríntios':'1 Corinthians','2 Coríntios':'2 Corinthians','Gálatas':'Galatians','Efésios':'Ephesians','Filipenses':'Philippians',
                'Colossenses':'Colossenses','1 Tessalonicenses':'1 Thessalonians','2 Tessalonicenses':'2 Thessalonians','1 Timóteo':'1 Timothy',
                '2 Timóteo':'2 Timothy','Tito':'Titus','Filemom':'Philemon','Hebreus':'Hebrews','Tiago':'James','1 Pedro':'1 Peter','2 Pedro':'2 Peter',
                '1 João':'1 John','2 João':'2 John','3 João':'3 John','Judas':'Jude','Apocalipse':'Revelation'
            };
            if (ptMap[book]) book = ptMap[book];
            const queries = splitRange(book, rest);
            let formattedContent = '<div class="space-y-3">';
            let foundAny = false;
            for (const q of queries) {
                if (q.raw !== undefined) {
                    // fallback single token
                    const encoded = encodeURIComponent(`${q.book} ${q.raw}`).replace(/%3A/g, ':').replace(/%2C/g, ',');
                    const data = await (await fetch(`https://bible-api.com/${encoded}?translation=almeida`)).json();
                    if (data.verses) { foundAny = true; formattedContent += formatVerses(data.verses); }
                    else if (data.text) { foundAny = true; formattedContent += `<p>${data.text.trim()}</p>`; }
                    continue;
                }
                const data = await fetchChapter(q.book, q.chapter);
                if (data && data.verses) {
                    foundAny = true;
                    const vs = data.verses.filter(v => verseInRange(v.verse, q));
                    formattedContent += formatVerses(vs.length ? vs : data.verses);
                } else if (data && data.text) {
                    foundAny = true;
                    formattedContent += `<p>${data.text.trim()}</p>`;
                }
            }
            if (!foundAny) formattedContent += '<p>Versículo não encontrado.</p>';
            formattedContent += '</div>';
            modalContent.innerHTML = formattedContent;
        } catch (error) {
            console.error('Erro ao buscar o versículo:', error);
            modalContent.innerHTML = '<p>Erro ao buscar o versículo.</p>';
        }
    }

    function formatVerses(verses) {
        let html = '<div class="space-y-1">';
        for (const verse of verses) {
            html += `<p><span class="font-bold text-xs align-top mr-1">${verse.verse}</span> ${verse.text.trim()}</p>`;
        }
        html += '</div>';
        return html;
    }

    // Event delegation to catch clicks even on nested elements
    document.addEventListener('click', (event) => {
        const link = event.target.closest('.verse-link, .ref, [data-reference]');
        if (!link) return;
        event.preventDefault();
        const reference = link.getAttribute('data-reference') || link.textContent.trim();
        if (reference) fetchVerse(reference);
    });
});
