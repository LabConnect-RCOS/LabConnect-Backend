import React from "react";
import Avatar from "../../shared/components/UIElements/Avatar";
import AboutSection from "./AboutSection";
import JobHeader from "./JobHeader";
import JobDescription from "./JobDescription";
import SmallTextButton from "./SmallTextButton";
import JobInteractionButton from "./JobInteractionButton";

const JobDetails = ({
  name,
  author,
  department,
  description,
  authorProfile,
  aboutSection,
  recommended_experience,
}) => {
  return (
    <article className="job-details-header">
      <JobHeader
        title={name}
        author={author}
        img={authorProfile}
        department={department}
      />
      <AboutSection aboutSection={aboutSection} />
      <JobDescription
        description={`${
          description ? description : "No description available."
        }`}
      />

      <JobDescription
        title="Recommended Experience"
        description={`${
          recommended_experience
            ? recommended_experience
            : "No recommended experience available."
        }`}
      />
    </article>
  );
};

export default JobDetails;
