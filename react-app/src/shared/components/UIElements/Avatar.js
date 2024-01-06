import React from "react";

const Avatar = ({ img, name, role }) => {
  return (
    <div className="flex align-items-center gap-3">
      <img className="rounded-full w-12 h-12" src={img} alt={name} />
      <div>
        <h5 className="text-blue-800 text-base">{name}</h5>
        <h6 className="text-sm">{role}</h6>
      </div>
    </div>
  );
};

export default Avatar;
