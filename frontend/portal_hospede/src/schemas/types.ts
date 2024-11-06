import { z } from "zod";

export const AmenitieSchema = z.object({
  id: z.number().positive().min(1),
  name: z.string(),
});

export const AccommodationSchema = z.object({
  ulid: z.string().ulid(),
  name: z.string(),
  status: z.string(),
  total_guests: z.number().positive().min(1),
  single_beds: z.number().nonnegative(),
  double_beds: z.number().nonnegative(),
  price: z.number().nonnegative(),
  amenities: z.array(AmenitieSchema),
});

export type Accommodation = z.infer<typeof AccommodationSchema>;

export type Amenitie = z.infer<typeof AccommodationSchema>;

export const BookingSearchParamSchema = z
  .object({
    checkin: z.string().date("A data de checkin deve ser uma data válida"),
    checkout: z.string().date("A data de checkout deve ser uma data válida"),
  })
  .refine(
    (schema) => {
      const checkIn = new Date(schema.checkin);
      const checkOut = new Date(schema.checkout);

      return checkOut > checkIn;
    },
    {
      message: "A data de checkout deve ser posterior à data de checkin",
      path: ["checkout"],
    }
  );

export type BookingSearchParam = z.infer<typeof BookingSearchParamSchema>;
