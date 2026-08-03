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
            'Salmos':'PSA','Psalmos':'PSA','Psalm':'PSA','Psalms':'PSA','Provérbios':'Proverbs','Eclesiastes':'Ecclesiastes','Cantares':'Song of Songs','Isaías':'Isaiah','Jeremias':'Jeremiah',
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
        const refs = [];
        for (const p of parts){
            // chapter range e.g. "8-9" -> fetch each chapter separately (API caps at 1 chapter)
            if (/^\d+-\d+$/.test(p)){
                const [a,b] = p.split('-').map(Number);
                for (let ch=a; ch<=b; ch++) refs.push(`${bookEn} ${ch}`);
                lastChapter = String(b);
                continue;
            }
            // verse range / single verse e.g. "8:1-5" or "8:1"
            if (/^\d+:\d+(?:-\d+)?$/.test(p)){
                lastChapter = p.split(':')[0];
                refs.push(`${bookEn} ${p}`);
                continue;
            }
            // bare verse number after a chapter:verse e.g. "6" -> "16:6"
            if (/^\d+$/.test(p) && lastChapter){
                refs.push(`${bookEn} ${lastChapter}:${p}`);
                continue;
            }
            // bare chapter number e.g. "15" -> whole chapter
            if (/^\d+$/.test(p)){
                refs.push(`${bookEn} ${p}`);
                lastChapter = p;
                continue;
            }
            refs.push(`${bookEn} ${p}`);
        }
        return refs.length ? refs : [`${bookEn} ${rest}`];
    }

    async function fetchVerse(reference) {
        openModal();
        const cleanedReference = reference.replace(/\+/g, ' ');
        modalTitle.textContent = cleanedReference;
        try {
            const refs = parseReferences(reference);
            const results = [];
            for (const r of refs){
                const encoded = encodeURIComponent(r).replace(/%3A/g, ':').replace(/%2C/g, ',');
                const response = await fetch(`https://bible-api.com/${encoded}`);
                const data = await response.json();
                results.push({r, data});
            }
            let formattedContent = '<div class="space-y-3">';
            for (const {data} of results){
                if (data.verses) {
                    formattedContent += '<div class="space-y-1">';
                    for (const verse of data.verses) {
                        formattedContent += `<p><span class="font-bold text-xs align-top mr-1">${verse.verse}</span> <strong>${verse.text.trim()}</strong></p>`;
                    }
                    formattedContent += '</div>';
                } else if (data.text) {
                    formattedContent += `<p>${data.text.trim()}</p>`;
                }
            }
            if (formattedContent === '<div class="space-y-3">'){
                formattedContent += '<p>Versículo não encontrado.</p>';
            }
            formattedContent += '</div>';
            modalContent.innerHTML = formattedContent;
        } catch (error) {
            console.error('Erro ao buscar o versículo:', error);
            modalContent.innerHTML = '<p>Erro ao buscar o versículo.</p>';
        }
    }

    // Event delegation to catch clicks even on nested elements
    document.addEventListener('click', (event) => {
        const link = event.target.closest('.verse-link, .ref');
        if (!link) return;
        event.preventDefault();
        const reference = link.getAttribute('data-reference') || link.textContent.trim();
        if (reference) fetchVerse(reference);
    });
});
