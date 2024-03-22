import React from "react";

const FeaturedImage = ({ className }) => {
  return (
    <figure
      className={`${className} featimage lg:min-w-96`}
    >
      <img
        src="https://research.rpi.edu/sites/default/files/styles/research_/public/2021-04/AdobeStock_90603827-scaled_x.png?itok=89zwJo_v"
        alt="Shoes"
      />
    </figure>
  );
};

export default FeaturedImage;
