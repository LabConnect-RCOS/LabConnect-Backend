import React from "react";
import ReactDOM from "react-dom";

const Backdrop = ({ onClick }) => {
  return ReactDOM.createPortal(
    <div onClick={onClick} className="backdrop" />,
    document.getElementById("backdrop-hook")
  );
};

export default Backdrop;
