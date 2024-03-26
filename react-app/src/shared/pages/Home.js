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
      <section className="flex flex-col h-screen justify-between">
      <section className="text-center justify-center font-sans text-lg">
        <br/>
        <img src="../../../LabConnect_Logo.png" alt="Logo" className="flex justify-center"></img>
        <br/>

        <p>
          Welcome to LabConnect!
        </p>
        <p>
          If you are a student looking to search for research opportunities, go to the <Link to="/jobs" className="no-underline"><b>Jobs</b></Link> tab to start.<br/>
          If you are a teacher, <Link className="no-underline"><b>Sign In</b></Link> and then go to <Link to="/createPost" className="no-underline"><b>Create</b></Link> to start posting opportunities
          or <Link to="/profile" className="no-underline"><b>Profile</b></Link> to view and edit your current posts.
        </p>
      </section>
      <section>
        <p className="text-center justify-center font-serif">
          An RCOS Project
        </p>
        <div className="flex flex-row">
          <img src="../../../LabConnect_Logo.png" alt="Logo" className="w-60 h-60"></img>
          <p className="justify-center">
            Contact Us:
            <p>
              dummyemail@gmail.com
            </p>
          </p>
        </div>
      </section>
    </section>
  );
};

export default Home;
