editButton = document.getElementById("edit_btn");

if (editButton instanceof HTMLButtonElement) {
  editButton.addEventListener("click", () => {
    const form = document.getElementById("edit-form");
    const data = {
      document: form.elements.document.value,
      name: form.elements.name.value,
      surname: form.elements.surname.value,
      country: form.elements.country.value,
      phone: form.elements.phone.value,
      created_at: form.elements.created_at.value,
    };
    fetch("http://127.0.0.1:5000/api/hospedes/", {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(() => {
        window.location.href = "http://127.0.0.1:5000/hospedes/";
      })
      .catch((e) => {
        console.log(e);
      });
  });
}

deleteButton = document.getElementById("delete_btn");

if (deleteButton instanceof HTMLButtonElement) {
  deleteButton.addEventListener("click", () => {
    const form = document.getElementById("edit-form");
    fetch(
      `http://127.0.0.1:5000/api/hospedes/${form.elements.document.value}`,
      {
        method: "DELETE",
      }
    )
      .then(() => {
        window.location.href = "http://127.0.0.1:5000/hospedes/";
      })
      .catch((e) => {
        console.log(e);
      });
  });
}
