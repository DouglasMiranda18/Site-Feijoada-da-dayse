let cart = [];

// Função para adicionar ao carrinho
function addToCartFromModal(button) {
    const produto = window.produtoAtualModal;
    const select = document.getElementById('modalTamanhoSelect');
    const size = select.value;

    if (!size) {
        alert("Por favor, selecione um tamanho.");
        return;
    }

    const price = parseFloat(select.options[select.selectedIndex].getAttribute("data-price"));

    cart.push({ name: produto.nome, size, price, quantity: 1 });
    updateCartDisplay();

    const popover = bootstrap.Popover.getInstance(button) || new bootstrap.Popover(button, {
        trigger: 'manual',
        placement: 'top'
    });

    popover.show();
    setTimeout(() => popover.hide(), 1500);

    mostrarPopoverCarrinho();
}


function mostrarPopoverCarrinho() {
    const carrinhoBtn = document.getElementById("iconeCarrinho");
    if (carrinhoBtn) {
        const popover = new bootstrap.Popover(carrinhoBtn, {
            trigger: 'manual',
            placement: 'bottom',
            content: 'Item adicionado!',
            customClass: 'popover-confirmado'
        });

        popover.show();

        const popoverElement = document.querySelector('.popover');
        if (popoverElement) {
            popoverElement.classList.add('bg-success', 'text-white');
        }

        setTimeout(() => popover.hide(), 1500);
    }
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartList = document.getElementById("cartList");
    const cartCount = document.getElementById("cartCount");
    cartList.innerHTML = '';
    cartCount.textContent = cart.length;

    let total = 0;
    cart.forEach((item, index) => {
        total += item.price * item.quantity;
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            ${item.name} (${item.size}) - R$ ${item.price.toFixed(2).replace('.', ',')}
            <button class="btn btn-sm btn-danger" onclick="removeFromCart(${index})">&times;</button>
        `;
        cartList.appendChild(li);
    });

    const totalLi = document.createElement('li');
    totalLi.className = 'list-group-item fw-bold';
    totalLi.innerHTML = `Total: R$ ${total.toFixed(2).replace('.', ',')}`;
    cartList.appendChild(totalLi);
}

function sendOrder() {
    const name = document.getElementById("customerName").value.trim();
    const phone = document.getElementById("customerPhone").value.trim();
    const address = document.getElementById("customerAddress").value.trim() || "Não informado";
    const payment = document.getElementById("paymentMethod").value.trim();

    let message = `Pedido via Feijoada da Dayse\n\n`;
    message += `*Nome:* ${name}\n`;
    message += `*Telefone:* ${phone}\n`;
    message += `*Endereço:* ${address}\n`;
    message += `*Forma de pagamento:* ${payment}\n\n`;
    message += `*Itens do pedido:*`;

    cart.forEach(item => {
        message += `\n- ${item.quantity}x ${item.name} - R$ ${(item.price * item.quantity).toFixed(2)}`;
    });

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    message += `\n\n*Total:* R$ ${total.toFixed(2)}`;

    const encodedMessage = encodeURIComponent(message);
    window.open(`https://wa.me/5581991143275?text=${encodedMessage}`, '_blank');
}

document.addEventListener("DOMContentLoaded", function () {
    const carrinhoBtn = document.getElementById("iconeCarrinho");
    if (carrinhoBtn) {
        const popover = new bootstrap.Popover(carrinhoBtn, {
            trigger: 'manual',
            placement: 'bottom',
            content: 'Item adicionado!',
            customClass: 'popover-confirmado'
        });

        // Exibe o popover do carrinho assim que a página carregar
        mostrarPopoverCarrinho();
    }
});
