const loadingPage = document.getElementById("loading_page");
const mainPage = document.getElementById("main");

function hideLoadingPage() {
    loadingPage.style.display = 'none';
    mainPage.style.display = 'block';
}

setTimeout(function () {
    hideLoadingPage();
}, 900);