from app.data.repositories.BookingRepository import BookingRepository


def list_all_bookings(bookingRepository: BookingRepository):
    existing_bookings = bookingRepository.find_many()
    result = []
    for existing_booking in existing_bookings:
        booking_dto = {
            "uuid": existing_booking.uuid,
            "created_at": existing_booking.created_at,
            "status": existing_booking.status,
            "guest": existing_booking.guest.to_dict(),
            "accommodation": existing_booking.accommodation.to_dict(),
            "check_in": existing_booking.check_in,
            "check_out": existing_booking.check_out,
            "total": str(existing_booking.calculate_budget()),
            "total_nights": str(existing_booking.calculate_period()),
        }
        result.append(booking_dto)

    return {"bookings": result}
