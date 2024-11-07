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

export const AccommodationListSchema = z.array(AccommodationSchema);

export type Accommodation = z.infer<typeof AccommodationSchema>;

export type Amenitie = z.infer<typeof AccommodationSchema>;

export const BookingSearchParamSchema = z
  .object({
    checkin: z
      .string()
      .date("A data de checkin deve ser uma data válida")
      .transform((value) => new Date(value)),
    checkout: z
      .string()
      .date("A data de checkout deve ser uma data válida")
      .transform((value) => new Date(value)),
  })
  .refine(({ checkin, checkout }) => checkout > checkin, {
    message: "A data de checkout deve ser posterior à data de checkin",
    path: ["checkout"],
  });

export type BookingSearchParam = z.infer<typeof BookingSearchParamSchema>;

export const guestSchema = z.object({
  ulid: z.string().ulid(),
  name: z.string(),
  surname: z.string(),
  phone: z.string(),
  country: z.string(),
});

export type Guest = z.infer<typeof guestSchema>;

export const bookingSchema = z.object({
  ulid: z.string().ulid(),
  status: z.string(),
  locator: z.string(),
  check_in: z.string().transform((value) => new Date(value)),
  check_out: z.string().transform((value) => new Date(value)),
  budget: z.number().nonnegative(),
  guest: guestSchema,
  accommodation: AccommodationSchema,
});

export type Booking = z.infer<typeof bookingSchema>;

export const bookingListSchema = z.array(bookingSchema);
