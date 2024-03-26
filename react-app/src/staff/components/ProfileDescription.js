import React from "react";

const ProfileDescription = ({className, name, researchCenter, department, description}) => {
  return (
    <div className={`${className} font-light flex2 gap-2`}>
      <h2 className="font-extrabold text-5xl">{name}</h2>
      <h5 className="text-gray-700">
        {researchCenter} {researchCenter && "·"} {department}
      </h5>
      <p>{description}</p>
    </div>
  );
};


export default ProfileDescription;