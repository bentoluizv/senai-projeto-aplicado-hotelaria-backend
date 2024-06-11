const form = document.querySelector(".form");
const submiter = document.querySelector(".submit_btn");

if (!form instanceof HTMLFormElement) throw new Error("Element not found");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = {
    document: form.elements.document.value
      .replace(".", "")
      .replace(".", "")
      .replace("-", ""),
    name: form.elements.name.value,
    surname: form.elements.surname.value,
    country: form.elements.country.value,
    phone: form.elements.phone.value,
  };

  fetch("http://127.0.0.1:5000/api/hospedes/cadastro", {
    method: "POST",
    body: JSON.stringify(data),
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
        console.log(json);
        errElement.textContent = `Hóspede com documento ${formData.document} já cadastrado`;

        errElement.classList.remove("hidden");
        setTimeout(() => {
          errElement.classList.add("hidden");
        }, 2500);
      });
    }
  });
});
