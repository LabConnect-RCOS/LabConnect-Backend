import React from "react";
import CreationForms from "../components/CreationForms";

// import ".staff.css";

const CreatePost = () => {
  return (
    <div className="flex justify-center mt-3">
      <div>
        <h1>Create Research Opportunity</h1>
        <CreationForms />
      </div>
    </div>
  );
};

export default CreatePost;
