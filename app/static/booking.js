



const tableBody = document.getElementById("table_content");

if (tableBody) {
  tableBody.addEventListener("click", (event) => {
    doc = event.target.parentNode.cells.namedItem("uuid").textContent;
    window.location.href = `http://127.0.0.1:5000/reservas/${uuid}`;
  });
}
