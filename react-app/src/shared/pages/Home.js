import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <section>
      Welcome to Labconnect!
      <br />
      This is the hub to find and apply to research on campus!
      <br />
      <Link to="/jobs">
        <button className="btn btn-primary">Find Jobs</button>
      </Link>
    </section>
  );
};

export default Home;
