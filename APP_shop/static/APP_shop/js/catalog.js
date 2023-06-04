


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



