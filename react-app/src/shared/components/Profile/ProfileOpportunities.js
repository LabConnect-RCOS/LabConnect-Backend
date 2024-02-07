import React from "react";
import OpportunityActionCard from "./OpportunityActionCard";
import { useState, useEffect } from "react";

const DUMMY_DATA = {
  d1: [
    {
      title: "Software Intern",
      body: "Posted February 8, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      activeStatus: true,
      id: "o1",
    },
    // create dummy data for the opportunities
    {
      title: "Biology Intern",
      body: "Due February 2, 2024",
      attributes: ["Paid", "Credits"],
      activeStatus: true,
      id: "o2",
    },
    {
      title: "Physics Intern",
      body: "Due February 6, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      activeStatus: true,
      id: "o3",
    },
    {
      title: "Chemistry Intern",
      body: "Due February 15, 2023",
      attributes: ["Remote", "Paid", "Credits"],
      activeStatus: true,
      id: "o4",
    },
    {
      title:
        "Mathematics Intern For the Sciences and Engineering Mathematics Intern For the Sciences and Engineering",
      body: "Due February 1, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      activeStatus: true,
      id: "o5",
    },
  ],
};

const ProfileOpportunities = ({ id }) => {
  var [opportunities, setOpportunities] = useState(false);

  const fetchOpportunities = async (key) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(DUMMY_DATA[key]);
      }, 5000);
    });
  };

  async function setData(key) {
    const response = await fetchOpportunities(key);
    response && setOpportunities(response);
    response || setOpportunities("no response");
  }

  useEffect(() => {
    setData("d1");
  }, []);

  async function changeOpportunityActiveStatus(opportunityId) {
    // send a request to the backend to deactivate the opportunity
    // if the request is successful, then deactivate the opportunity from the list
    const response = true;

    if (response) {
      const newOpportunities = opportunities.map((opportunity) =>
      opportunity.id === opportunityId
        ? { ...opportunity, activeStatus: !opportunity.activeStatus } // Spread operator for update
        : opportunity
    );

      setOpportunities(newOpportunities);
    }
  }

  async function deleteOpportunity(opportunityId) {
    // send a request to the backend to delete the opportunity
    // if the request is successful, then delete the opportunity from the list
    const response = true;

    if (response) {
      opportunities = opportunities.filter(
        (opportunity) => opportunity.id !== opportunityId
      );
    } else {
      alert("Failed to delete opportunity");
    }

    setOpportunities(opportunities);
    console.log(opportunities);
  }

  var opportuntityList = (
    <div>
      <h1>Posted Opportunties</h1>
      <div className="flex gap-2 flex-wrap">
        {opportunities &&
          opportunities.map((opportunity) => (
            <OpportunityActionCard
              editPath={`/editPost/${opportunity.id}`}
              id={opportunity.id}
              activeStatus={opportunity.activeStatus}
              changeActiveStatus={changeOpportunityActiveStatus}
              deleteOpp={deleteOpportunity}
              title={opportunity.title}
              body={opportunity.body}
              key={opportunity.id}
            />
          ))}
      </div>
    </div>
  );

  return opportunities ? (
    opportuntityList
  ) : opportunities === "no response" ? (
    "No opportunities found"
  ) : (
    <span className="loading loading-dots loading-lg" />
  );
};

export default ProfileOpportunities;
