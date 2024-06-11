const select = document.querySelector(".resource_menu");
const searchButton = document.querySelector(".search_btn");
const searchInput = document.querySelector(".search_field");

searchButton.addEventListener("click", () => {
  const model = select.value;
  const content = searchInput.value;

  // TODO: Validar o conteudo de 'content'

  if (model == "hospede") {
    fetch(`http://127.0.0.1:5000/api/hospedes/${content}`).then((response) => {
      if (response.status == 404) {
        response.json().then((json) => {
          console.log(JSON.stringify(json));
          // TODO:  Ativar  menssagem de erro na tela
        });
      }
      if (response.status == 200) {
        response.json().then((json) => {
          window.location.href = `http://127.0.0.1:5000/hospedes/${content}`;
        });
      }
    });
  }

  if (model == "reserva") {
    fetch(`http://127.0.0.1:5000/api/reservas/${content}`).then((response) => {
      if (response.status == 404) {
        response.json().then((json) => {
          console.log(JSON.stringify(json));
          // TODO:  Ativar  menssagem de erro na tela
        });
      }
      if (response.status == 200) {
        response.json().then((json) => {
          window.location.href = `http://127.0.0.1:5000/reservas/${content}`;
        });
      }
    });
  }
});
