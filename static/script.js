// ================= ADD NOTE MODAL =================

function openAddModal() {

    const modal = document.getElementById("addModal");

    if (modal) {
        modal.style.display = "flex";
    }
}


function closeAddModal() {

    const modal = document.getElementById("addModal");

    if (modal) {
        modal.style.display = "none";
    }
}


// ================= EDIT NOTE MODAL =================

function openEditModal(id, title, content) {

    const modal = document.getElementById("editModal");

    const titleInput = document.getElementById("editTitle");

    const contentInput = document.getElementById("editContent");

    const form = document.getElementById("editForm");


    if (modal && titleInput && contentInput && form) {

        titleInput.value = title;

        contentInput.value = content;

        form.action = "/edit_note/" + id;

        modal.style.display = "flex";
    }
}


function closeEditModal() {

    const modal = document.getElementById("editModal");

    if (modal) {
        modal.style.display = "none";
    }
}


// ================= DELETE CONFIRMATION =================

function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this note?"
    );
}


// ================= CLOSE MODAL =================

window.addEventListener("click", function(event) {

    const addModal = document.getElementById("addModal");

    const editModal = document.getElementById("editModal");


    if (event.target === addModal) {
        closeAddModal();
    }


    if (event.target === editModal) {
        closeEditModal();
    }

});


// ================= AUTO HIDE ALERT =================

setTimeout(function() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function(alert) {

        alert.style.transition = "opacity 0.5s";

        alert.style.opacity = "0";

        setTimeout(function() {
            alert.remove();
        }, 500);

    });

}, 4000);