import React from "react";
import FeaturedImage from "./FeaturedImage";
import ProfileDescription from "./ProfileDescription";

const CenterHero = () => {
  return (
    <div className="flex justify-center">
      <div className="flex2 lg:flex-row gap-5">
        <FeaturedImage />
        <ProfileDescription
          name={"CBIS"}
          description={`This Center enables new lines of research in web science, high-performance computing, artificial intelligence, data science, and predictive analytics and links them to applications in a vast range of areas, from cybersecurity to health and environmental preservation.`}
        />
      </div>
    </div>
  );
};

export default CenterHero;
