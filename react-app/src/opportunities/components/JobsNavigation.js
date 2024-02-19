import React from "react";
import { useLocation } from "react-router";

const JobsNavigation = ({ jobPage, switchPage }) => {
  const path = useLocation().pathname;

  const activeLink = "active-link";
  const normalLink = "normal-link";

  

  return (
    <div className="flex gap-5" style={{ alignItems: "center" }}>
      <h1 className="jobs-header">Jobs</h1>

      <nav
        className="jobs-categories"
        style={{ alignItems: "center" }}
      >
        <button
          onClick={switchPage}
          className={jobPage ? activeLink : normalLink}
        >
          Search
        </button>
        <button
          onClick={switchPage}
          className={jobPage ? normalLink : activeLink}
        >
          Saved
        </button>
      </nav>
    </div>
  );
};

export default JobsNavigation;
