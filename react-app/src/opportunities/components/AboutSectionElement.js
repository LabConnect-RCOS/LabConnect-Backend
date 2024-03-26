import React from "react";

const AboutSectionElement = ({ title, description }) => {
  return (
    <div className="about-head">
      <h5 className="about-title">{title}</h5>
      <h6 className="about-description">{description}</h6>
    </div>
  );
};

export default AboutSectionElement;
