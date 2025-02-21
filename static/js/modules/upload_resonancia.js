
Fancybox.bind("[data-fancybox]", {
    Toolbar: {
      display: ["close"],
    },
    Image: {
      zoom: true,
    },
  });

document.addEventListener("DOMContentLoaded", function () {
    const submitForm = document.getElementById("submitForm");
    const submitBtn = document.getElementById("submitBtn");
    const flair = document.getElementById("flair");
    const t1ce = document.getElementById("t1ce");
    const openModalBtn = document.getElementById("openModalBtn");
    const confirmSaveButton = document.getElementById("confirmSaveButton");

    if (submitForm) {

      submitForm.addEventListener("submit", function (e) {
  
        if (!flair.files.length || !t1ce.files.length) {
          e.preventDefault(); 
          alert("Por favor, selecciona ambos archivos.");
        } else {
   
          submitBtn.disabled = true;
          submitBtn.textContent = "Procesando...";
        }
      });
    }


    if (openModalBtn) {
      openModalBtn.addEventListener("click", function () {
        $("#confirmModal").modal("show");
      });
    }


    if (confirmSaveButton) {
      confirmSaveButton.addEventListener("click", function () {

        const confirmInput = document.createElement("input");
        confirmInput.type = "hidden";
        confirmInput.name = "confirm_save";
        confirmInput.value = "1";
        submitForm.appendChild(confirmInput);
        submitForm.submit();
        $("#confirmModal").modal("hide");
      });
    }
  });