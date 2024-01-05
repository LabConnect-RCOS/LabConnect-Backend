import React from "react";
import { useLocation } from "react-router";

const JobsNavigation = ({ jobPage, switchPage }) => {
  const path = useLocation().pathname;

  const activeLink = "text-black py-3 border-b-2 border-black text-lg";
  const normalLink =
    "text-gray-600 py-3 text-lg hover:border-b-2 border-black hover:text-black";

  return (
    <div className="flex gap-5" style={{ alignItems: "center" }}>
      <h1 className="text-2xl font-bold">Jobs</h1>

      <nav
        className="text-base flex gap-4 justify-items-center font-semibold"
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
