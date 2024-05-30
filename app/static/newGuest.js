const form = document.querySelector(".form");
const submiter = document.querySelector(".submit_btn");

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
  }).then((res) => {
    if (res.status == 201) {
      window.location.href = "http://127.0.0.1:5000/hospedes";
    }

    if (res.status == 409) {
      errElement = document.querySelector(".err_msg");

      res.json().then((json) => {
        errElement.textContent = json.description;

        errElement.classList.remove("hidden");
        setTimeout(() => {
          errElement.classList.add("hidden");
        }, 3000);
      });
    }
  });
});
