submitBtn = document.getElementById("submit_btn");

if (submitBtn instanceof HTMLButtonElement) {
  submitBtn.addEventListener("click", () => {
    window.location.href = "http://127.0.0.1:5000/hospedes/cadastro/";
  });
}
