import React from "react";

const FeaturedImage = ({ className }) => {
  return (
    <figure
      className={`${className} min-w-32 lg:min-w-96 w-96 h-72 bg-base-100 shadow-xl rounded-md overflow-clip`}
    >
      <img
        src="https://research.rpi.edu/sites/default/files/styles/research_/public/2021-04/AdobeStock_90603827-scaled_x.png?itok=89zwJo_v"
        alt="Shoes"
      />
    </figure>
  );
};

export default FeaturedImage;
