import React from "react";
import SmallTextButton from "./SmallTextButton";

const FiltersField = () => {
  return (
    <div>
      <hr />
      <div className="px-3 overflow-x-scroll max-h-20 ">
        <SmallTextButton>All Filters</SmallTextButton>
      </div>
      <hr />
    </div>
  );
};

export default FiltersField;
