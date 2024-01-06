import React from "react";
import { useState } from "react";
import JobPost from "./JobPost";

let DUMMY_JOBS = [
  {
    title: "Software Engineer",
    professor: "Turner",
    id: "u1",
    location: "CII",
    season: "Spring",
    year: 2024,
  },
  {
    title: "Biology Researcher",
    professor: "Turner",
    id: "u2",
    location: "CII",
    season: "Spring",
    year: 2024,
  },
];

const PostsField = () => {
  var [activeId, setActiveId] = useState("u1");
    
  return (
    <div>
      {DUMMY_JOBS.map((job)=>{
        return <JobPost active={job.id==activeId} onClick={setActiveId} key={job.id} {...job} />
      })}
    </div>
  );
};

export default PostsField;
