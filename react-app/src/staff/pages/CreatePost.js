import React from "react";
import CreationForms from "../components/CreationForms";

const CreatePost = ({edit}) => {
  return (
    <div className="flex justify-center mt-3">
      <div>
        <h1>{edit==true ? "Edit Research Opportunity" : "Create Research Opportunity"}</h1>
        <CreationForms />
      </div>
    </div>
  );
};

export default CreatePost;
