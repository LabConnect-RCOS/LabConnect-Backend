import React from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <section>
      Welcome to Labconnect!
      <br />
      This is the hub to find and apply to research on campus!
      <br />
      <Link to="/jobs">
        <Button>Find Jobs</Button>
      </Link>
    </section>
  );
};

export default Home;
