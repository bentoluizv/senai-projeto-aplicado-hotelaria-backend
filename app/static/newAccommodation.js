const form = document.querySelector(".form");
const submiter = document.querySelector(".submit_btn");

fetch("http://127.0.0.1:5000/api/amenities").then((res) => {
  json = res.json().then((data) => {
    const amenitieList = document.querySelector(".amenitie_list");
    for (const amenitie of data) {
      const div = document.createElement("div");
      const label = document.createElement("label");
      label.htmlFor = amenitie["amenitie"];
      label.textContent = amenitie["amenitie"];
      const input = document.createElement("input");
      input.type = "checkbox";
      input.id = amenitie["amenitie"];
      input.name = amenitie["amenitie"];
      div.appendChild(input);
      div.appendChild(label);
      amenitieList.appendChild(div);
    }
  });
});

if (!form instanceof HTMLFormElement) throw new Error("Element not found");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  formDataIterator = new FormData(form, submiter);
  let formData = {};
  for ([key, value] of formDataIterator) {
    formData[key] = value;
  }

  const amenities = [];
  const data = {};

  for (const property in formData) {
    if (formData[property] == "on") {
      amenities.push(property);
    } else {
      data[property] = formData[property];
    }
  }

  data.amenities = amenities;
  fetch("http://127.0.0.1:5000/api/acomodacoes/cadastro", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => {
    if (res.status == 201) {
      window.location.href = "http://127.0.0.1:5000/acomodacoes";
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
