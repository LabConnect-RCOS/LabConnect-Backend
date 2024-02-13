import React from "react";
import LargeTextCard from "./LargeTextCard";

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
      title: "Mathematics Intern For the Sciences and Engineering Mathematics Intern For the Sciences and Engineering",
      body: "Due February 1, 2024",
      attributes: ["Remote", "Paid", "Credits"],
      id: "o5",
    },
  ],
};

const ProfileOpportunities = ({ id }) => {
  return (
    <div>
      <h1>Posted Opportunties</h1>
      <div className="flex gap-2 flex-wrap">
        {id &&
          DUMMY_DATA[id].map((opportunity) => (
            <LargeTextCard
              to={`/post/${opportunity.id}`}
              title={opportunity.title}
              body={opportunity.body}
              attributes={opportunity.attributes}
              key={opportunity.id}
            />
          ))}
      </div>
    </div>
  );
};

export default ProfileOpportunities;
