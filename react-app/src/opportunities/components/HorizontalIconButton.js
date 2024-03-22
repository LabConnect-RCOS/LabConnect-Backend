import React, { Children } from "react";

const HorizontalIconButton = ({ children, onClick, icon, special }) => {
  return (
    <div
      className={`${special && "font-medium"} ${
        !special && "font-sm"
      } horizontal-btn`}
    >
      <button
        className="hover:text-red-600"
        onClick={() => {
          onClick(children);
        }}
      >
        {icon}
      </button>
      {children}
    </div>
  );
};

export default HorizontalIconButton;
