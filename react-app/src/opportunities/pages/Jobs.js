import React, { useState } from "react";
import JobsNavigation from "../components/JobsNavigation";
import { Router, Routes, Route } from "react-router-dom";
import Posts from "../components/Posts";
import SavedJobs from "../components/SavedJobs";
import PageNavigation from "../../shared/components/Navigation/PageNavigation";
import usePageNavigation from "../../shared/hooks/page-navigation-hook";
import StickyFooter from "../../shared/components/Navigation/StickyFooter.js"

const Jobs = () => {
  var [pages, switchPage] = usePageNavigation(["Search", "Saved"], "Search");

  return (
    <section className="flex flex-col h-screen justify-between gap-3">
      <section className="flex2 gap-3">
        <section>
          <PageNavigation
            title="Jobs"
            pages={pages}
            switchPage={switchPage}
          />

          {pages.activePage==="Search" && <Posts />}
        </section>
      </section>
      <StickyFooter/>
    </section>
  );
};

export default Jobs;
