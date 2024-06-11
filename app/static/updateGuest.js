const saveBtn = document.querySelector(".submit_btn");

saveBtn.addEventListener("click", () => {
  const form = document.querySelector(".form");

  const data = {
    document: form.elements.document.value,
    name: form.elements.name.value,
    surname: form.elements.surname.value,
    country: form.elements.country.value,
    phone: form.elements.phone.value,
    created_at: form.elements.created_at.value,
  };

  fetch("http://127.0.0.1:5000/api/hospedes", {
    method: "PUT",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (res.status == 201) {
        window.location.href = "http://127.0.0.1:5000/hospedes";
      }
    })
    .catch((e) => {
      console.log(e);
    });
});

const deleteBtn = document.querySelector(".delete_btn");

deleteBtn.addEventListener("click", () => {
  const form = document.querySelector(".form");
  const doc = form.elements.document.value;
  fetch(`http://127.0.0.1:5000/api/hospedes/${form.elements.document.value}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (res.status == 200) {
        window.location.href = "http://127.0.0.1:5000/hospedes";
      }
    })
    .catch((e) => {
      console.log(e);
    });
});
