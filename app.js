function toggleHeader() {
    let links = document.getElementById("links");
    let menu_title = document.getElementById("menu-link-text");

    // Toggle between none and block
    links.style.display = (links.style.display ===  "block") ? "none" : "block";
    menu_title.innerHTML = (links.style.display === "block") ? "Close" : "Menu";
}

// Toggle drop down when header is clicked
document.getElementById("header").addEventListener("click", toggleHeader);