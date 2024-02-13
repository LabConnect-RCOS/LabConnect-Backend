import React from "react";
import Avatar from "../../shared/components/UIElements/Avatar";
import AboutSection from "./AboutSection";
import JobHeader from "./JobHeader";
import JobDescription from "./JobDescription";
import SmallTextButton from "./SmallTextButton";
import JobInteractionButton from "./JobInteractionButton";

const JobDetails = ({
  title,
  author,
  department,
  description,
  authorProfile,
  aboutSection,
}) => {
  return (
    <article className="job-details-header">
      <JobHeader
        title={title}
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
    </article>
  );
};

export default JobDetails;
