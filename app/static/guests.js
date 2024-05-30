const submitBtn = document.querySelector(".submit_btn");

submitBtn.addEventListener("click", () => {
  window.location.href = "http://127.0.0.1:5000/hospedes/cadastro";
});

const tableBody = document.getElementById("table_content");

if (tableBody) {
  tableBody.addEventListener("click", (event) => {
    doc = event.target.parentNode.cells.namedItem("document").textContent;
    window.location.href = `http://127.0.0.1:5000/hospedes/${doc}`;
  });
}
