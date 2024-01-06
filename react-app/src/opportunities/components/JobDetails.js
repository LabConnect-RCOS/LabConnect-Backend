import React from "react";
import Avatar from "../../shared/components/UIElements/Avatar";
import AboutSection from "./AboutSection";
import JobHeader from "./JobHeader";
import JobDescription from "./JobDescription";
import SmallTextButton from "./SmallTextButton";
import JobInteractionButton from "./JobInteractionButton";

const JobDetails = ({title,author, department, description, authorProfile}) => {
  return (
    <article className="w-full col-span-7 border-l border-r p-24 flex flex-col gap-5 shadow-sm">
      <JobHeader
        title={title}
        author={author}
        img={authorProfile}
        department={department}
      />
      <AboutSection />
      <JobDescription
        description={`${description ? description : "No description available."}`}
      />
      
    </article>
  );
};

export default JobDetails;
