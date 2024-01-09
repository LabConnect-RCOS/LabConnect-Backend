import React from "react";
import Avatar from "./Avatar";

const AvatarCard = ({ img, name, role, className }) => {
  return (
    <div className={className}>
      <Avatar img={img} name={name} role={role} className="p-2 border rounded min-w-fit max-w-fit" />
    </div>
  );
};

export default AvatarCard;
