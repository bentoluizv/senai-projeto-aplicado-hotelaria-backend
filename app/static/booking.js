document.addEventListener("DOMContentLoaded", function() {
  const searchBtn = document.getElementById("search_btn");
  const searchField = document.getElementById("search");
  const resourceMenu = document.getElementById("resource");

  searchBtn.addEventListener("click", function() {
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



