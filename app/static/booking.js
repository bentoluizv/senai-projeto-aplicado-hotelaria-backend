document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("search_btn");
  const searchField = document.getElementById("search");
  const resourceMenu = document.getElementById("resource");

  searchBtn.addEventListener("click", function () {
    const searchValue = searchField.value;
    const resourceValue = resourceMenu.value;
    if (searchValue && resourceValue) {
      window.location.href = `/reservas/${encodeURIComponent(resourceValue)}/${encodeURIComponent(searchValue)}`;
    }
  });
});

const submitBtn = document.querySelector(".search_btn");

submitBtn.addEventListener("click", () => {
  window.location.href = "http://127.0.0.1:5000/reservas/pesquisa";
});


const tableBody = document.getElementById("table_content");

if (tableBody) {
  tableBody.addEventListener("click", (event) => {
    doc = event.target.parentNode.cells.namedItem("uuid").textContent;
    window.location.href = `http://127.0.0.1:5000/reservas/${uuid}`;
  });

}

const booking_btn = document.querySelector(".booking_btn");

booking_btn.addEventListener("click", () => {
  window.location.href = "http://127.0.0.1:5000/reservas/cadastro";
});

document.addEventListener('DOMContentLoaded', function () {

  fetch('http://127.0.0.1:5000/api/reservas')
    .then(response => response.json())
    .then(data => {

      const documentList = document.getElementById('documentList');

      function updateDocumentList() {
        documentList.innerHTML = '';
        const resourceValue = document.getElementById("resource").value;

        data.forEach(reserva => {
          if (resourceValue === "hospede") {
            const option = document.createElement('option');
            option.value = reserva.guest.document;
            documentList.appendChild(option);
          } else {
            const option = document.createElement('option');
            option.value = reserva.uuid;
            documentList.appendChild(option);
          }
        });
      }

      // Ouvinte de evento para monitorar mudanças no campo resource
      document.getElementById("resource").addEventListener("change", updateDocumentList);
      updateDocumentList();


    })
    .catch(error => console.error('Error fetching documents:', error));
});

