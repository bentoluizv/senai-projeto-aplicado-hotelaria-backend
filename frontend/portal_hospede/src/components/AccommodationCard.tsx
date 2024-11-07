import { FunctionComponent } from "react";
import { Accommodation } from "../schemas/types";

interface AccommodationCardProps {
  accommodation: Accommodation;
  onSelect: (id: string) => void;
  selected: boolean;
}

const AccommodationCard: FunctionComponent<AccommodationCardProps> = ({
  accommodation,
  onSelect,
  selected,
}) => {
  return (
    <div
      onClick={() => onSelect(accommodation.ulid)}
      className={`p-4 border rounded-lg cursor-pointer ${
        selected ? "bg-blue-100 border-blue-500" : "bg-white border-gray-300"
      }`}>
      <h2 className="text-lg font-bold">{accommodation.name}</h2>
      <p className="text-sm text-gray-500">Status: {accommodation.status}</p>
      <p className="text-sm">Total Guests: {accommodation.total_guests}</p>
      <p className="text-sm">Price: ${accommodation.price.toFixed(2)}</p>
      <div className="text-sm mt-2">
        <h3 className="font-medium">Amenities:</h3>
        <ul className="list-disc list-inside">
          {accommodation.amenities.map((amenity, index) => (
            <li key={index}>{amenity.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AccommodationCard;
