import { FunctionComponent } from "react";
import { images } from "../shared/images";

const BackgroundImage: FunctionComponent = () => {
  return (
    <div className="flex overflow-hidden h-screen">
      {images.map((image) => (
        <img
          key={image.id}
          className="object-cover w-full h-full"
          src={image.src}
          alt={image.alt}
        />
      ))}
    </div>
  );
};

export default BackgroundImage;
