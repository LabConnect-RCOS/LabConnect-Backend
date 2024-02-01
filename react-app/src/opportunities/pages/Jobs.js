import React, { useState } from "react";
import JobsNavigation from "../components/JobsNavigation";
import { Router, Routes, Route } from "react-router-dom";
import Posts from "../components/Posts";
import SavedJobs from "../components/SavedJobs";
import PageNavigation from "../../shared/components/Navigation/PageNavigation";
import usePageNavigation from "../../shared/hooks/page-navigation-hook";

const Jobs = () => {
  var [pages, switchPage] = usePageNavigation(["Search", "Saved"], "Search");

  return (
    <section className="flex flex-col gap-3">
      <PageNavigation
        title="Jobs"
        pages={pages}
        switchPage={switchPage}
      />

      {pages.activePage==="Search" && <Posts />}
    </section>
  );
};

export default Jobs;
