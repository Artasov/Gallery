const pagContainer = document.querySelector('.pag_container');

function sendFavoritesToServer() {
    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    if (favorites.length > 0) {
        let url = `/shop/get_favorite_products_bt_names?items=${encodeURIComponent(JSON.stringify(favorites))}`;
        fetch(url)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    document.getElementById('not-found').classList.remove('d-none');
                }
            })
            .then(data => {
                data.forEach(el => {
                    const pag_el = createPagEl(el);
                    pagContainer.appendChild(pag_el);
                });
            })
            .catch(error => {
                document.getElementById('not-found').classList.remove('d-none');
            });
    } else {
        document.getElementById('not-found').classList.remove('d-none');
    }
}

sendFavoritesToServer();
