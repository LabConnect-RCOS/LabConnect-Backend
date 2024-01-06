import React from "react";
import { useState } from "react";
import JobPost from "./JobPost";
import JobDetails from "./JobDetails";

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

const DUMMY_DATA = [
  {
    title: "Software Engineer",
    description: "Lorem Ipsum",
    author: "John Smith",
    id: "u1",
    author:"https://thedailyq.org/wp-content/uploads/2018/02/H-Menge-Torsten-900x600.jpg",
    department:"Computer Science"
  },
  {
    title: "Physics Research Intern",
    description: "Lorem Ipsum",
    author: "John Smith",
    id: "u2",
    authorProfile:"https://thedailyq.org/wp-content/uploads/2018/02/H-Menge-Torsten-900x600.jpg",
    department:"Physics"
  }
];

const PostsField = ({ activeId, setActive }) => {
  const findJobDetails = (id) => {
    return DUMMY_DATA.find((item)=>item.id===id);
  }
  
  return (
    <div className="border-t border-b grid grid-cols-9">
      <div className="col-span-2">
        {DUMMY_JOBS.map((job) => {
          return (
            <JobPost
              active={job.id == activeId}
              onClick={setActive}
              key={job.id}
              {...job}
            />
          );
        })}
      </div>
      <JobDetails
        {...(findJobDetails(activeId))}
      />
    </div>
  );
};

export default PostsField;
