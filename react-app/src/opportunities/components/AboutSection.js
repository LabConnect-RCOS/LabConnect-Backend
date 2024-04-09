import React from "react";
import AboutSectionElement from "./AboutSectionElement";

const AboutSection = ({ aboutSection }) => {
  let i = 0;

  return (
    <section className="flex2 gap-3">
      <h3 className="about-role">About the role</h3>

      <div className="about-map" style={{ rowGap: "1rem" }}>
        {aboutSection.map((item) => {
          return (
            <AboutSectionElement
              key={++i}
              title={item.title}
              description={item.description}
            />
          );
        })}
      </div>
    </section>
  );
};

export default AboutSection;
