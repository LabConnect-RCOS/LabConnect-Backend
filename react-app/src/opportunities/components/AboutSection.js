import React from "react";
import AboutSectionElement from "./AboutSectionElement";

const AboutSection = ({ aboutSection }) => {
  let i = 0;

  return (
    <section className='flex flex-col gap-3'>
      <h3 className='font-extrabold text-3xl'>About the role</h3>

      <div className='grid grid-cols-3' style={{ rowGap: "1rem" }}>
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
