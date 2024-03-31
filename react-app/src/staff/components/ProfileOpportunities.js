import React from "react";
import LargeTextCard from "./LargeTextCard";

import { useState, useEffect } from "react";
import { type } from "@testing-library/user-event/dist/type";

const DUMMY_DATA = {
  d1: [
    {
      title: "Software Intern",
      body: "Posted February 8, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      id: "o1",
    },
    // create dummy data for the opportunities
    {
      title: "Biology Intern",
      body: "Due February 2, 2024",
      attributes: ["Paid", "Credits"],
      id: "o2",
    },
    {
      title: "Physics Intern",
      body: "Due February 6, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      id: "o3",
    },
    {
      title: "Chemistry Intern",
      body: "Due February 15, 2023",
      attributes: ["Remote", "Paid", "Credits"],
      id: "o4",
    },
    {
      title:
        "Mathematics Intern For the Sciences and Engineering Mathematics Intern For the Sciences and Engineering",
      body: "Due February 1, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      id: "o5",
    },
  ],
};

// create fetch request to get the opportunities
const fetchOpportunities = async (id) => {
  // Consider moving the base URL to a configuration
  const baseURL = "http://localhost:8000";
  const url = `${baseURL}/getProfessorOpportunityCards/led`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Network response was not ok - Status: ${response.status}`);
  }

  const data = await response.json();
  console.log(data);
  return data;
};

const ProfileOpportunities = ({ id }) => {
  var [opportunities, setOpportunities] = useState(false);

  const fetchOpportunities = async (key) => {
    // Consider moving the base URL to a configuration
    const baseURL = "http://localhost:8000";
    const url = `${baseURL}/getProfessorOpportunityCards/led`;

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(
        `Network response was not ok - Status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log(data);
    return data["data"];
  };

  async function setData(key) {
    const response = await fetchOpportunities(key);
    response && setOpportunities(response);
    response || setOpportunities("no response");
  }

  useEffect(() => {
    setData(id);
  }, [id]);

  var opportunityList = (
    <div className="flex gap-2 flex-wrap">
      {id && opportunities && typeof opportunities === "object" &&
        opportunities.map((opportunity) => (
          <LargeTextCard
            to={`/post/${opportunity.id}`}
            title={opportunity.title}
            body={opportunity.body}
            attributes={opportunity.attributes}
            key={opportunity.id}
          />
        ))}
    </div>
  );

  return (
    <div>
      <h1>Posted Opportunties</h1>
      {opportunities ? opportunityList : "Loading..."}
      {opportunities === "no response" && "No Opportunities Found"}
    </div>
  );
};

export default ProfileOpportunities;
