import React from "react";

const JobsNavigation = () => {
  return (
    <div className="container-xl flex gap-5" style={{ alignItems: "center" }}>
      <h1 className="text-2xl font-bold">Jobs</h1>

      <nav
        className="flex gap-3 justify-items-center"
        style={{ alignItems: "center" }}
      >
        <div>search</div>
        <div>saved</div>
      </nav>
    </div>
  );
};


export default JobsNavigation;