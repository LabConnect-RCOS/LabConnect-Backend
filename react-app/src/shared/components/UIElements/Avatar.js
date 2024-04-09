import React from "react";

const Avatar = ({ img, name, role, className }) => {
  return (
    <div className={`${className} avatar1`}>
      <img className="avatar-img" src={img} alt={name} />
      <div>
        <h5 className="avatar-name">{name}</h5>
        <h6 className="text-sm">{role}</h6>
      </div>
    </div>
  );
};

export default Avatar;
