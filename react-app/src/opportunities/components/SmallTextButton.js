import React, { Children } from "react";

const SmallTextButton = ({ children, onClick, icon, special, className }) => {
  return (
    <div className={`${className}`}>
      <button
        onClick={onClick}
        className={`${special && "font-medium"} ${
          !special && "font-sm"
        } flex align-items-center p-2 px-2.5 rounded-3xl border hover:text-blue-700 hover:border-blue-700`}
      >
        {children}
      </button>
    </div>
  );
};

export default SmallTextButton;
