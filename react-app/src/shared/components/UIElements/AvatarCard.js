import React from "react";
import Avatar from "./Avatar";

const AvatarCard = ({ img, name, role, className }) => {
  return (
    <div className={className}>
      <Avatar img={img} name={name} role={role} className="avatar-card" />
    </div>
  );
};

export default AvatarCard;
