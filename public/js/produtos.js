const lista = JSON.parse(localStorage.getItem('produtos')) || [];

function exibirProdutos() {
    const productList = document.getElementById("productList");
    productList.innerHTML = "";

    lista.forEach((produto, index) => {
        if (!produto.nome || !produto.descricao || !produto.imagem || !produto.tamanho) {
            console.error(`Produto com índice ${index} está faltando dados obrigatórios!`);
            return;
        }

        const col = document.createElement("div");
        col.className = "col-6 col-md-4";

        const tamanhos = Object.entries(produto.tamanho).map(([key, price]) => {
            if (!key || !price) {
                console.error(`Tamanho ou preço inválido para o produto ${produto.nome}.`);
                return '';
            }
            return `<option value="${key}" data-price="${price}">${key} - R$ ${price.toFixed(2)}</option>`;
        }).join("");

        col.innerHTML = `
            <div class="card product-card shadow-sm border-0 rounded-4 h-100">
                <img src="${produto.imagem}" class="card-img-top rounded-top-4" alt="${produto.nome}" style="height: 200px; object-fit: cover; object-position: center back;" />
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title fw-bold">${produto.nome}</h5>
                    <p class="card-text">${produto.descricao}</p>
                    <div class="mt-auto d-grid gap-2">
                        <button class="btn btn-outline-primary" onclick="abrirDetalhes(${index})">
                            <i class="bi bi-info-circle"></i> Ver Detalhes
                        </button>
                    </div>
                </div>
            </div>
        `;

        productList.appendChild(col);
    });
}

function abrirDetalhes(index) {
    const produto = lista[index];

    const offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('cartModal'));
    if (offcanvas) {
        offcanvas.hide();
    }

    document.getElementById('modalImagem').src = produto.imagem;
    document.getElementById('modalNome').textContent = produto.nome;

    const tamanhosHtml = Object.entries(produto.tamanho).map(([key, price]) => {
        return `<option value="${key}" data-price="${price}">${key} - R$ ${price.toFixed(2)}</option>`;
    }).join("");

    document.getElementById('modalTamanhoSelect').innerHTML = tamanhosHtml;
    document.getElementById('modalDescricao').textContent = produto.descricao;

    window.produtoAtualModal = produto;

    const modal = new bootstrap.Modal(document.getElementById('modalDetalhes'));
    modal.show();
}

document.addEventListener("DOMContentLoaded", exibirProdutos);