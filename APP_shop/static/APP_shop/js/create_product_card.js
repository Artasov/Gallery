function createPagEl(pagJsonEl) {
    const col = document.createElement('div');
    col.classList.add('col', 'py-1', 'px-1');

    const card = document.createElement('div');
    card.classList.add('card', 'h-100', 'rounded-4', 'position-relative');
    col.appendChild(card);

    let likeBtn = document.createElement('div');
    likeBtn.setAttribute('product_name', pagJsonEl.name.toString());
    likeBtn.classList.add('like_btn');
    likeBtn.style.width = '40px';
    likeBtn.style.height = '40px';
    let likeImg = document.createElement('img');
    likeImg.setAttribute('src', '/media/img/heart.png/');
    likeImg.classList.add('w-100', 'h-100');
    likeImg.style.objectFit = 'cover';
    likeBtn.appendChild(likeImg);
    if(isInLocalStorage(pagJsonEl.name.toString())){
        likeBtn.classList.toggle('like_btn-active');
    }
    likeBtn.addEventListener('click', function () {
        const product_name = this.getAttribute('product_name');
        addToFavorites(product_name);
        this.classList.toggle('like_btn-active');
    })
    card.appendChild(likeBtn);


    const img = document.createElement('img');
    img.classList.add('card-img-top', 'rounded-top-4');
    img.src = pagJsonEl.image;
    img.alt = '...';
    card.appendChild(img);

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');
    card.appendChild(cardBody);

    const cardTitle = document.createElement('h5');
    cardTitle.classList.add('card-title');
    cardTitle.textContent = pagJsonEl.name;
    cardBody.appendChild(cardTitle);

    const cardText = document.createElement('p');
    cardText.classList.add('card-text');
    cardText.textContent = pagJsonEl.description;
    cardBody.appendChild(cardText);

    const listGroup = document.createElement('ul');
    listGroup.classList.add('list-group', 'list-group-flush', 'rounded-bottom-4');
    card.appendChild(listGroup);

    if (pagJsonEl.size !== null) {
        const sizeItem = document.createElement('li');
        sizeItem.classList.add('list-group-item');
        sizeItem.textContent = `Размер: ${pagJsonEl.size}`;
        listGroup.appendChild(sizeItem);
    }
    if (pagJsonEl.proba !== null) {
        const probaItem = document.createElement('li');
        probaItem.classList.add('list-group-item');
        probaItem.textContent = `Проба: ${pagJsonEl.proba}`;
        listGroup.appendChild(probaItem);
    }
    if (pagJsonEl.weight !== null) {
        const weightItem = document.createElement('li');
        weightItem.classList.add('list-group-item');
        weightItem.textContent = `Вес: ~${pagJsonEl.weight}`;
        listGroup.appendChild(weightItem);
    }

    return col;
}