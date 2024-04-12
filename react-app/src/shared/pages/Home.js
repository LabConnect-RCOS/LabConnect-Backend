import React, { useEffect } from "react";
import useAuthActions from "../../context/global/authActions";
import { Link } from "react-router-dom";
import StickyFooter from "../components/Navigation/StickyFooter.js";

import logo from "../../images/LabConnect_Logo.png"; 
console.log(logo);

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
      <section className="home-general">
        <br/><br/><br/>
        <div className="img-center">
          <img src={logo} alt="Logo" />

        </div>

        <br/><br/><br/><br/>

        <p className="text-xl">
          Welcome to LabConnect!
        </p>
        <p className="text-base">
          If you are a student, go to the <Link to="/jobs" className="no-underline"><b>Jobs</b></Link> tab to view currently available research opportunities.<br/>
          If you are a professor or staff member, <Link className="no-underline"><b>Sign In</b></Link> and then go to <Link to="/createPost" className="no-underline"><b>Create</b></Link> to start posting <br/>
          opportunities or <Link to="/profile" className="no-underline"><b>Profile</b></Link> to view and edit your current posts.
        </p>
        <br/><br/><br/>
      </section>
    </section>
  );
};

export default Home;
