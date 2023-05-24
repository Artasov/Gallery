const categoryArrowLeft = document.getElementById('category-arrow-left');
const categoryArrowRight = document.getElementById('category-arrow-right');
const categoryScrollBlock = document.getElementsByClassName('category-menu_wrapper')[0];


categoryArrowLeft.addEventListener('click', function () {
    categoryScrollBlock.scrollBy({
        left: -140,
        behavior: 'smooth'
    });
});

categoryArrowRight.addEventListener('click', function () {
    categoryScrollBlock.scrollBy({
        left: 140,
        behavior: 'smooth'
    });
});


let last_pag_num = 0;
const pagBlockScroll = document.querySelector('.pag_block_scroll');
const pagContainer = document.querySelector('.pag_container');
pagBlockScroll.addEventListener('scroll', pag_container_onscroll);
const errorMargin = 10;
let access_upload = true;

let metal = '';
let category = '';

const btnGold = document.getElementById('btn-gold');
const btnSilver = document.getElementById('btn-silver');
const btnAll = document.getElementById('btn-all');
btnGold.addEventListener('click', function () {
    metal = 'gold';
    pagContainer.innerHTML = "";
    last_pag_num = 0;
    const btnsMetalSelect = document.getElementsByClassName('btn-metal-select ');
    for (let i = 0; i < btnsMetalSelect.length; i++) {
        btnsMetalSelect[i].classList.remove('btn-1-active');
    }
    this.classList.add('btn-1-active');
    pag_container_onscroll();
})
btnSilver.addEventListener('click', function () {
    metal = 'silver';
    pagContainer.innerHTML = "";
    last_pag_num = 0;
    const btnsMetalSelect = document.getElementsByClassName('btn-metal-select ');
    for (let i = 0; i < btnsMetalSelect.length; i++) {
        btnsMetalSelect[i].classList.remove('btn-1-active');
    }
    this.classList.add('btn-1-active');
    pag_container_onscroll();
})
btnAll.addEventListener('click', function () {
    metal = '';
    pagContainer.innerHTML = "";
    last_pag_num = 0;
    const btnsMetalSelect = document.getElementsByClassName('btn-metal-select ');
    for (let i = 0; i < btnsMetalSelect.length; i++) {
        btnsMetalSelect[i].classList.remove('btn-1-active');
    }
    this.classList.add('btn-1-active');
    pag_container_onscroll();
})

const categoryItems = document.getElementsByClassName('category_menu-item');
for (let i = 0; i < categoryItems.length; i++) {
    categoryItems[i].addEventListener('click', function () {
        if (access_upload) {
            category = this.getAttribute('value');
            pagContainer.innerHTML = "";
            last_pag_num = 0;
            for (let j = 0; j < categoryItems.length; j++) {
                categoryItems[j].classList.remove('category-active');
            }
            this.classList.add('category-active');
            pag_container_onscroll();
        }
    })
}

pag_container_onscroll();

function pag_container_onscroll() {
    if (!access_upload) {
        return;
    }
    if (pagBlockScroll.offsetHeight + pagBlockScroll.scrollTop + errorMargin >= pagBlockScroll.scrollHeight) {
        access_upload = false;
        fetch(`/shop/get_new_for_pagination/${last_pag_num}/?category=${category}&metal=${metal}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data_json => {
                if (!data_json.end) {
                    data_json.forEach(pag => {
                        const pag_el = createPagEl(pag);
                        pagContainer.appendChild(pag_el);
                        last_pag_num += 1;
                    });
                }
                access_upload = true;
            })
            .catch(error => {
                // console.error('An error occurred while fetching the data: ', error);
            });
    }
}



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