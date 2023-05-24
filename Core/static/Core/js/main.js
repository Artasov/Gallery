function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

window.onload = function (e) {
    document.getElementById('loading_spinner_block').remove();
    document.getElementById('content').classList.remove('d-none');
}

function addToFavorites(item) {
    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    if (!favorites.includes(item)) {
        favorites.push(item);
        localStorage.setItem("favorites", JSON.stringify(favorites));
    } else {
        removeFromFavorites(item);
    }
}

// Функция removeFromFavorites удаляет элемент из локального хранилища
function removeFromFavorites(item) {
    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    if (favorites.includes(item)) {
        favorites = favorites.filter((fav) => fav !== item);
        localStorage.setItem("favorites", JSON.stringify(favorites));
    } else {
        addToFavorites(item);
    }
}

function showFavorites() {
    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    if (favorites.length === 0) {
        return null;
    } else {
        return favorites;
    }
}
function isInLocalStorage(item) {
  let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
  return favorites.includes(item);
}