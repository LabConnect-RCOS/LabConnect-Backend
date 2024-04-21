import React, { useEffect } from "react";
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
    authorProfile:
      "https://thedailyq.org/wp-content/uploads/2018/02/H-Menge-Torsten-900x600.jpg",
    department: "Computer Science",
    aboutSection: [
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
    ],
  },
  {
    title: "Biology Reseacher",
    description: "Lorem Ipsum",
    author: "Turner",
    id: "u2",
    authorProfile:
      "https://thedailyq.org/wp-content/uploads/2018/02/H-Menge-Torsten-900x600.jpg",
    department: "Biology",
    aboutSection: [
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
      {
        title: "Application Deadline",
        description: "July 1, 2024, 12pm",
      },
    ],
  },
];

const PostsField = ({ activeId, setActive, opportunities }) => {
  const findJobDetails = (id) => {
    return DUMMY_DATA.find((item) => item.id === id);
  };
  
  var [activeOpportunity, setActiveOpportunity] = useState(null);
  
  const fetchOpportunity = async (id) => {
    const url = `http://localhost:8000/getOpportunity/${id}`;
    const response = await fetch(url);
    if (!response.ok) {
      console.log("Error fetching opportunity");
      setActiveOpportunity(null);
    } else {
      let data = await response.json();
      data = data.data;
      setActiveOpportunity(data);
    }
  }
  
  useEffect(() => {
    fetchOpportunity(activeId);
  }, [activeId]);

  return (
    <div className="postsfield-header">
      <div className="col-span-2">
        {opportunities && opportunities.map((job) => {
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
      {activeId != "" && activeOpportunity && <JobDetails {...activeOpportunity} />}
      {(activeId == "" || !activeOpportunity) && "Opportunity not found."}
    </div>
  );
};

export default PostsField;
