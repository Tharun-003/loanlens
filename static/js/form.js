document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", () => {
            const loader = form.querySelector(".loading");
            if (loader) {
                loader.style.display = "flex";
            }
        });
    });
});
