import { useState } from "react";
import { FieldValues } from "react-hook-form";
import AccommodationList from "./components/AccommodationList";
import BackgroundImage from "./components/BackgroundImage";
import Form from "./components/Form";
import Modal from "./components/Modal";

function App() {
  const [visibility, setVisibility] = useState<boolean>(false);

  const onSubmit = (fieldValues: FieldValues) => {
    console.log(fieldValues);
  };

  return (
    <>
      <h1 className="sr-only">Faça sua Reserva</h1>
      <main className="flex justify-center items-center">
        <BackgroundImage />

        <div className="absolute w-full flex gap-5 justify-center">
          <Form onSubmit={onSubmit} />
        </div>

        <Modal isOpen={visibility}>
          <AccommodationList accommodations={[]} />
          <button
            onClick={() => setVisibility(false)}
            className="text-amber-50 text-lg">
            Fechar
          </button>
        </Modal>
      </main>
    </>
  );
}

export default App;
