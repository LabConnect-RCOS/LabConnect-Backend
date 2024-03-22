import React from "react";

const JobPost = ({
  title,
  professor,
  id,
  location,
  season,
  year,
  onClick,
  active,
}) => {
  return (
    <div className="job-post-header">
      <div className={`${active && "border-l-2 border-l-purple-600"}`} />
      <div
        onClick={() => {
          onClick(id);
        }}
        className="job-post-btn hover:bg-gray-100 p-1 rounded hover:cursor-pointer"
      >
        <h4 className="job-post-title">{title}</h4>
        <div className="">
          <h5 className="job-post-description">{professor}</h5>
          <h5 className="job-post-description">
            {location} · {season} {year}
          </h5>
        </div>
      </div>
    </div>
  );
};

export default JobPost;
