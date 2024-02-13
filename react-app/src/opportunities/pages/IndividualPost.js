import React, { useState } from "react";
import JobDetails from "../components/JobDetails";
import { useParams } from "react-router";
import { useEffect } from "react";
import { set } from "react-hook-form";

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

const IndividualPost = () => {
  const { postID } = useParams();

  const findJobDetails = (id) => {
    return DUMMY_DATA.find((item) => item.id === id);
  };
  
  async function getDetails(id) {
    // fetch details from server
    // wait 5 seconds 
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(findJobDetails(id));
      }, 5000);
    });
  }
  
  async function findDetails(id) {
    var data = await getDetails(id);
    details = data || "Nothing found";
    setDetails(details);
  }

  var [details, setDetails] = useState("Searching");

  useEffect(() => {
    findDetails(postID);
  }, []);

  return (
    <div>
      {details == "Searching" ? (
        <span className="loading loading-spinner loading-lg" />
      ) : details == "Nothing found" ? (
        <p>No post found</p>
      ) : (
        <JobDetails {...details} />
      )}
    </div>
  );
};

export default IndividualPost;
