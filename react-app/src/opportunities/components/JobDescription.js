import React from "react";

const JobDescription = ({ title, description }) => {
  return (
    <article className="job-desc-header">
      <div className="job-desc-title">{title || "Role Description"}</div>

      <div className="job-desc-description">{description}</div>
    </article>
  );
};

export default JobDescription;
