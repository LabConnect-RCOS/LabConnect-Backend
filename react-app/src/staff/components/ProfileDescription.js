import React from "react";

const ProfileDescription = ({name, researchCenter, department, description}) => {
  return (
    <div className="font-light flex flex-col gap-2">
      <h2 className="font-extrabold text-5xl">{name}</h2>
      <h5 className="text-gray-700">
        {researchCenter} {researchCenter && "·"} {department}
      </h5>
      <p>{description}</p>
    </div>
  );
};


export default ProfileDescription;