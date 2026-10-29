document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".searchinput");
    const categorySelect = document.querySelector(".categoryselect");
    const resourceBoxes = document.querySelectorAll(".exampleboxes");

    function filterResources() {
        const searchValue = searchInput.value.toLowerCase();
        const selectedCategory = categorySelect.value;

        resourceBoxes.forEach(box => {
            const boxCategory = box.getAttribute("data-category");
            const textContent = box.innerText.toLowerCase();

            const matchesSearch = textContent.includes(searchValue);
            const matchesCategory =
                selectedCategory === "all" || boxCategory === selectedCategory;

            if (matchesSearch && matchesCategory) {
                box.style.display = "block";
            } else {
                box.style.display = "none";
            }
        });
    }

    searchInput.addEventListener("keyup", filterResources);
    categorySelect.addEventListener("change", filterResources);
});
