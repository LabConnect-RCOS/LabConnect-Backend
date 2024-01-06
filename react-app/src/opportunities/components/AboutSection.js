import React from "react";
import AboutSectionElement from "./AboutSectionElement";

const AboutSection = () => {
  return (
    <section className="flex flex-col gap-3">
      <h3 className="font-extrabold text-3xl">About the role</h3>

      <div className="grid grid-cols-3" style={{ rowGap: "1rem" }}>
        <AboutSectionElement
          title={"Application Deadline"}
          description={"July 1, 2024 9:00 AM"}
        />
        <AboutSectionElement
          title={"Application Deadline"}
          description={"July 1, 2024 9:00 AM"}
        />
        <AboutSectionElement
          title={"Application Deadline"}
          description={"July 1, 2024 9:00 AM"}
        />
        <AboutSectionElement
          title={"Application Deadline"}
          description={"July 1, 2024 9:00 AM"}
        />
        <AboutSectionElement
          title={"Application Deadline"}
          description={"July 1, 2024 9:00 AM"}
        />
      </div>
    </section>
  );
};

export default AboutSection;
