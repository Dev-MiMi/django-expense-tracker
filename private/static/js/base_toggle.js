const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const dropdownToggle = document.querySelector(".dropdown-toggle");
const dropdownMenu = document.querySelector(".dropdown-menu");
const themeToggle = document.getElementById("theme-toggle");


menuToggle.addEventListener("click", () => {
    const isActive = sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
    sidebar.setAttribute("aria-expanded", isActive);
});

overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
    sidebar.setAttribute("aria-expanded", "false");
    if (dropdownMenu) {
        dropdownMenu.classList.remove("active");
        dropdownToggle.setAttribute("aria-expanded", "false");
    }
});

if (dropdownToggle) {
    dropdownToggle.addEventListener("click", (event) => {
        event.preventDefault();
        const isActive = dropdownMenu.classList.toggle("active");
        dropdownToggle.setAttribute("aria-expanded", isActive);
    });
}

document.querySelectorAll("#sidebar a").forEach(link => {
    link.addEventListener("click", (event) => {
        const href = link.getAttribute("href");
        if (!href || href === "#") {
            event.preventDefault();
            return;
        }
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
        sidebar.setAttribute("aria-expanded", "false");
        if (dropdownMenu) {
            dropdownMenu.classList.remove("active");
            dropdownToggle.setAttribute("aria-expanded", "false");
        }
    });
});


themeToggle.addEventListener("click", () => {
    document.documentElement.dataset.theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
});
