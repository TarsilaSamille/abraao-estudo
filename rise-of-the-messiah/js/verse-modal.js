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

    async function fetchVerse(reference) {
        openModal();
        modalTitle.textContent = reference;
        try {
            const response = await fetch(`https://bible-api.com/${reference}?translation=almeida`);
            const data = await response.json();

            if (data.verses) {
                let formattedContent = '<div class="space-y-2">';
                for (const verse of data.verses) {
                    formattedContent += `<p><span class="font-bold text-xs align-top mr-1">${verse.verse}</span> ${verse.text.trim()}</p>`;
                }
                formattedContent += '</div>';
                modalContent.innerHTML = formattedContent;
            } else if (data.text) {
                modalContent.innerHTML = `<p>${data.text.trim()}</p>`;
            } else {
                modalContent.innerHTML = `<p>Versículo não encontrado.</p>`;
            }
        } catch (error) {
            console.error("Erro ao buscar o versículo:", error);
            modalContent.innerHTML = "<p>Erro ao buscar o versículo.</p>";
        }
    }

    document.querySelectorAll(".verse-link").forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const reference = link.getAttribute("data-reference");
            fetchVerse(reference);
        });
    });
});
