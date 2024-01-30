import React from "react";

const ProfileAvatar = ({image, name}) => {
  return (
    <div className="avatar">
      <div className="w-min h-min lg:w-36 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
        <img src={image} alt={name} />
      </div>
    </div>
  );
};

export default ProfileAvatar;
