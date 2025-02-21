document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".btn_desvincular").addEventListener("click", function() {
      const accountId = this.getAttribute("data-account-id");

      Swal.fire({
        title: "¿Estás seguro de desvincular tu cuenta de Google?",
        text: "¡Este cambio no se podrá revertir!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, desvincular",
        cancelButtonText: "No, cancelar",
        customClass: {
          confirmButton: "btn btn-success",
          cancelButton: "btn btn-danger"
        }
      }).then((result) => {
        if (result.isConfirmed) {
          fetch("{% url 'security:desvincular_cuenta' %}", {
            method: "POST",
            headers: {
              "X-CSRFToken": "{{ csrf_token }}",
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ account_id: accountId })
          })
          .then(response => response.json())
          .then(data => {
            console.log("Respuesta recibida del servidor:", data);
            if (data.success) {
              Swal.fire("¡Cuenta desvinculada!", data.message, "success").then(() => {
                location.reload(); 
              });
            } else {
              Swal.fire("Error", data.message, "error");
            }
          })
          .catch(error => {
            console.error("Error en la desvinculación:", error);
            Swal.fire("Error", "Ocurrió un error al intentar desvincular la cuenta.", "error");
          });
        }
      });
    });
});
