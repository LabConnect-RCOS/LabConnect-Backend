import React from "react";
import ReactDOM from 'react-dom';


const Backdrop = () => {
    return ReactDOM.createPortal(
      <div className="backdrop">
        {/* Add content or styling as needed here */}
      </div>,
      document.getElementById("backdrop-hook")
    );
  }

export default Backdrop;