document.addEventListener("DOMContentLoaded", function() {
    const recordTypeField = document.getElementById("id_record_type");
    const accountField = document.getElementById("id_account").closest("p");
    const fromAccountField = document.getElementById("id_from_account").closest("p");
    const toAccountField = document.getElementById("id_to_account").closest("p");

    function toggleFields() {
        const type = recordTypeField.value;

        if (type === "transfer") {
            accountField.style.display = "none";
            fromAccountField.style.display = "";
            toAccountField.style.display = "";
        } else {
            accountField.style.display = "";
            fromAccountField.style.display = "none";
            toAccountField.style.display = "none";
        }
    }

    recordTypeField.addEventListener("change", toggleFields);
    toggleFields();
});
