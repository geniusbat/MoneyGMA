function DisplayMenu() {
    let menu = document.getElementById("mainMenu");
    if (menu.style.display == "none") {
        menu.style.display = "flex";
    }
    else {
        menu.style.display = "none";
    }
}