document.addEventListener('DOMContentLoaded', function () {
  // Fetch hospedes
  fetch('http://127.0.0.1:5000/api/hospedes')
      .then(response => response.json())
      .then(data => {
          const documentList = document.getElementById('documentList');
          data.forEach(hospede => {
              const option = document.createElement('option');
              option.value = hospede.document;
              documentList.appendChild(option);
          });
      })
      .catch(error => console.error('Error fetching documents:', error));

  // Fetch acomodacoes
  fetch('http://127.0.0.1:5000/api/acomodacoes')
      .then(response => response.json())
      .then(data => {
          const acomodacaoList = document.getElementById('acomodacaoList');
          data.forEach(acomodacao => {
              const option = document.createElement('option');
              option.value = acomodacao.name;
              option.setAttribute('data-uuid', acomodacao.uuid);
              acomodacaoList.appendChild(option);
          });
      })
      .catch(error => console.error('Error fetching accommodations:', error));

  const form = document.querySelector('.form');
  form.addEventListener('submit', function (event) {
      const documentInput = document.getElementById('document');
      const documentValue = documentInput.value;
      const documentOptions = document.getElementById('documentList').options;
      let documentValid = false;

      for (let i = 0; i < documentOptions.length; i++) {
          if (documentValue === documentOptions[i].value) {
              documentValid = true;
              break;
          }
      }

      if (!documentValid) {
          event.preventDefault();
          const errMsg = document.querySelector('.err_msg');
          errMsg.textContent = 'Por favor, selecione um documento válido da lista.';
          errMsg.classList.remove('hidden');
      }

      const acomodacaoInput = document.getElementById('acomodacao');
      const acomodacaoValue = acomodacaoInput.value;
      const acomodacaoOptions = document.getElementById('acomodacaoList').options;
      let acomodacaoValid = false;

      for (let i = 0; i < acomodacaoOptions.length; i++) {
          if (acomodacaoValue === acomodacaoOptions[i].value) {
              acomodacaoValid = true;
              const uuid = acomodacaoOptions[i].getAttribute('data-uuid');
              document.getElementById('acomodacaoUuid').value = uuid;
              break;
          }
      }

      if (!acomodacaoValid) {
          event.preventDefault();
          const errMsg = document.querySelector('.err_msg');
          errMsg.textContent = 'Por favor, selecione uma acomodação válida da lista.';
          errMsg.classList.remove('hidden');
      }
  });
});