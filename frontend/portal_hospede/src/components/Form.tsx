import { zodResolver } from "@hookform/resolvers/zod";
import { FunctionComponent } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { BookingSearchParam, BookingSearchParamSchema } from "../schemas/types";

interface FormProps {
  onSubmit: (fieldValues: FieldValues) => void;
}

const Form: FunctionComponent<FormProps> = ({ onSubmit }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<BookingSearchParam>({
    resolver: zodResolver(BookingSearchParamSchema),
  });

  return (
    <form
      onSubmit={handleSubmit((fieldValues) => onSubmit(fieldValues))}
      className="p-4 rounded-md flex flex-col gap-4 bg-zinc-900/60 text-zinc-200 md:min-w-[360px]">
      <h2 className="sr-only">Escolha o Periodo</h2>
      <div className="flex flex-col">
        <label className="text-lg poppins-light-italic" htmlFor="checkin">
          Check In
        </label>
        <input
          {...register("checkin")}
          className="p-2 rounded-sm border-none text-zinc-800"
          id="checkin"
          name="checkin"
          type="date"
        />
        {errors.checkin?.message && (
          <p className="text-red-500 font-bold">{errors.checkin?.message}</p>
        )}
      </div>
      <div className="flex flex-col">
        <label className="text-lg poppins-light-italic" htmlFor="checkout">
          Check Out
        </label>
        <input
          {...register("checkout")}
          className="p-2 rounded-sm border-none text-zinc-800"
          id="checkout"
          name="checkout"
          type="date"
        />
        {errors.checkout?.message && (
          <p className="text-red-500 font-bold">{errors.checkout?.message}</p>
        )}
      </div>

      <button className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75">
        Buscar
      </button>
    </form>
  );
};

export default Form;
