import React, { useEffect } from "react";
import useAuthActions from "../../context/global/authActions";
import { Link } from "react-router-dom";

const Home = ({signOut, signIn}) => {
  
  const {login, logout} = useAuthActions();
  
  useEffect(() => {
    if (signOut) {
      logout();
    }
    
    if (signIn) {
      login();
    }
  }, []);
  
  return (
    <section>
      Welcome to Labconnect!
      <br />
        This is the hub to find and apply to research on campus!
      <br />
      <Link to="/jobs">
        <button className="btn2">Find Jobs</button>
      </Link>
    </section>
  );
};

export default Home;
