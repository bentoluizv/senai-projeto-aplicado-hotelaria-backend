const submitBtn = document.querySelector(".submit_btn");

submitBtn.addEventListener("click", () => {
  window.location.href = "http://127.0.0.1:5000/acomodacoes/cadastro";
});

const tableBody = document.getElementById("table_content");

tableBody.addEventListener("click", (event) => {
  const uuid = event.target.parentNode.cells.namedItem("uuid").textContent;
  window.location.href = `http://127.0.0.1:5000/acomodacoes/${uuid}`;
});
