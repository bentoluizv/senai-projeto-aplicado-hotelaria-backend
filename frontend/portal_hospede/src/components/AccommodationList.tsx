import { FunctionComponent, useState } from "react";
import { Accommodation } from "../schemas/types";
import AccommodationCard from "./AccommodationCard";

interface AccommodationListProps {
  accommodations: Accommodation[];
}

const AccommodationList: FunctionComponent<AccommodationListProps> = ({
  accommodations,
}) => {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleSelect = (id: string) => {
    setSelectedId(id === selectedId ? null : id); // Toggle de seleção
  };
  return (
    <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
      {accommodations.map((accommodation) => (
        <AccommodationCard
          key={accommodation.ulid}
          accommodation={accommodation}
          onSelect={handleSelect}
          selected={selectedId === accommodation.ulid}
        />
      ))}
    </div>
  );
};

export default AccommodationList;
