import React, { useState } from "react";
import JobsNavigation from "../components/JobsNavigation";
import { Router, Routes, Route } from "react-router-dom";
import Posts from "../components/Posts";
import SavedJobs from "../components/SavedJobs";

const Jobs = () => {
  const [jobPage, setJobPage] = useState(true);
  
  const switchPage = () => {
    setJobPage(()=>!jobPage);
  }
    
  return (
    <main className="container-xl flex flex-col gap-3">
        
      <JobsNavigation jobPage={jobPage} switchPage={switchPage} />
      
      {jobPage && <Posts/>}
      
      
    </main>
  );
};

export default Jobs;
