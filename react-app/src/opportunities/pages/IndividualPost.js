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
  
  var [details, setDetails] = useState("Searching");

  const fetchOpportunities = async () => {
    // Consider moving the base URL to a configuration
    const baseURL = "http://localhost:8000";
    const url = `${baseURL}/getOpportunity/${postID}`;

    const response = await fetch(url);

    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    console.log(data);
    return data["data"];
  };

  async function findDetails() {
    var data = await fetchOpportunities();
    details = data || "Nothing found";
    setDetails(details);
  }


  useEffect(() => {
    findDetails();
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
