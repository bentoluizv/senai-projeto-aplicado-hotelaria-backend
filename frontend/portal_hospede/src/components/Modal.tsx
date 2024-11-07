import { FunctionComponent, useEffect, useRef } from "react";

interface ModalProps {
  isOpen: boolean;
  children: React.ReactNode;
}

const Modal: FunctionComponent<ModalProps> = ({ isOpen, children }) => {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (isOpen) {
      dialog?.showModal();
    } else {
      dialog?.close();
    }
  }, [isOpen]);

  return (
    <dialog
      ref={dialogRef}
      className="w-screen h-screen max-w-5xl rounded-md bg-zinc-900/90">
      <div
        aria-hidden={true}
        className="container mx-auto h-full flex flex-col items-center text-amber-50">
        {children}
      </div>
    </dialog>
  );
};

export default Modal;
