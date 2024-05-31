fetch("http://127.0.0.1:5000/api/amenities")
  .then((res) => {
    json = res.json().then((data) => {
      for (const amenitie of data) {
        const amenitieList = document.querySelector(".amenitie_list");
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
  })
  .then(() => {
    let uuid4 = "";

    paths = window.location.pathname.split("/");
    for (const pathname of paths) {
      if (isUUID(pathname)) {
        uuid4 = pathname;
      }
    }

    fetch(`http://127.0.0.1:5000/api/acomodacoes/${uuid4}`).then((res) => {
      res.json().then((accommodation) => {
        const checkboxes = document.querySelectorAll(
          '.amenitie_list input[type="checkbox"]'
        );
        for (const checkbox of checkboxes) {
          if (accommodation.amenities.includes(checkbox.name)) {
            checkbox.checked = true;
          }
        }
      });
    });
  });

const form = document.querySelector(".form");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = {
    uuid: form.elements.uuid.value,
    createdAt: form.elements.created_at.value,
    name: form.elements.name.value,
    totalGuests: form.elements.total_guests.value,
    singleBeds: form.elements.single_beds.value,
    doubleBeds: form.elements.double_beds.value,
    minNights: form.elements.min_nights.value,
    price: form.elements.price.value,
    amenities: [],
  };

  const checkboxes = document.querySelectorAll(
    '.amenitie_list input[type="checkbox"]'
  );

  for (const checkbox of checkboxes) {
    if (checkbox.checked) {
      data.amenities.push(checkbox.name);
    }
  }

  fetch("http://127.0.0.1:5000/api/acomodacoes", {
    method: "PUT",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (res.status == 201)
        window.location.href = "http://127.0.0.1:5000/acomodacoes";
    })
    .catch((e) => {
      console.log(e);
    });
});

const deleteBtn = document.querySelector(".delete_btn");

deleteBtn.addEventListener("click", () => {
  fetch(`http://127.0.0.1:5000/api/acomodacoes/${uuid.value}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (res.status == 200)
        window.location.href = "http://127.0.0.1:5000/acomodacoes";
    })
    .catch((e) => {
      console.log(e);
    });
});

function isUUID(string) {
  const regex =
    /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

  return regex.test(string);
}
