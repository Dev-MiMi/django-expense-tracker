document.addEventListener("DOMContentLoaded", () => {
    // === Categories behaviour ===
    const categoryMenu = document.getElementById("categoryMenu");
    const categoryCheckboxes = categoryMenu.querySelectorAll("input[type='checkbox']");
    const categoryBadge = document.getElementById("categoryBadge");

    categoryCheckboxes.forEach(cb => {
        cb.addEventListener("change", updateCategoryCount);
    });

    function updateCategoryCount() {
        const selected = Array.from(categoryCheckboxes).filter(cb => cb.checked).length;
        categoryBadge.textContent = `${selected} selected`;
        categoryBadge.classList.toggle("bg-primary", selected > 0);
        categoryBadge.classList.toggle("bg-secondary", selected === 0);
    }
    updateCategoryCount();

    // === Accounts behaviour with currency lock ===
    const accountMenu = document.getElementById("accountMenu");
    const accountCheckboxes = accountMenu.querySelectorAll("input[type='checkbox']");
    const accountsDisplay = document.getElementById("selectedAccountsDisplay");
    const currencyField = document.getElementById("currencyField");

    accountCheckboxes.forEach(cb => {
        cb.addEventListener("change", handleAccountSelection);
    });

    function handleAccountSelection() {
        const selectedAccounts = Array.from(accountCheckboxes).filter(cb => cb.checked);
        const selectedNames = selectedAccounts.map(cb => {
            const label = cb.nextElementSibling.textContent.trim();
            return label.split(' (')[0];  // Extract name only
        }).join(", ");
        accountsDisplay.textContent = selectedNames || "None selected";

        // Lock currency & disable incompatible accounts
        if (selectedAccounts.length > 0) {
            const currency = selectedAccounts[0].dataset.currency;
            currencyField.value = currency;

            accountCheckboxes.forEach(cb => {
                if (cb.dataset.currency !== currency && !cb.checked) {
                    cb.disabled = true;
                    cb.parentElement.classList.add("text-muted");
                } else {
                    cb.disabled = false;
                    cb.parentElement.classList.remove("text-muted");
                }
            });
        } else {
            currencyField.value = "";
            accountCheckboxes.forEach(cb => {
                cb.disabled = false;
                cb.parentElement.classList.remove("text-muted");
            });
        }
    }
    handleAccountSelection();
});
