function updatePrice(select, priceElement) {
    const selectedOption = select.options[select.selectedIndex];
    const price = selectedOption.getAttribute("data-price");
    priceElement.querySelector(".price").innerText = price;
}

function updateBlurBg() {
    const activeItem = document.querySelector('#carouselBanner .carousel-item.active img');
    const blurBg = document.querySelector('.carousel-blur-bg');

    if (activeItem && blurBg) {
        blurBg.style.backgroundImage = `url('${activeItem.src}')`;
    }
}

function toggleMenu() {
    document.querySelector('.nav-menu').classList.toggle('active');
}
