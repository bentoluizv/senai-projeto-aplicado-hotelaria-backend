form = document.getElementById("register_form");
submiter = document.getElementById("submit_btn");

if (!form instanceof HTMLFormElement) throw new Error("Element not found");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  formDataIterator = new FormData(form, submiter);
  let formData = {};
  for ([key, value] of formDataIterator) {
    formData[key] = value;
  }

  fetch("http://127.0.0.1:5000/api/hospedes/cadastro", {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (res.status == 201) {
        window.location.href = "http://127.0.0.1:5000/hospedes";
      }
    })
    .catch((err) => {
      console.log(err);
    });
});
