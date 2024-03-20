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
      <br />
      <img src="../../../LabConnect_Logo.png" alt="Logo" className="flex justify-center"></img>
      <br />
      <section className="text-center justify-center font-sans">
        <p>
          Welcome to LabConnect!
        </p>
        <p>
          If you are a student looking to search for research opportunities, go to the <Link to="/jobs">Jobs</Link> tab to start.<br/>
          If you are a teacher, go to <Link to="/createPost">Create Post</Link> to start posting opportunities or <Link to="/profile">Profile</Link> to view and edit your current posts.
        </p>
      </section>
      
      
      

    </section>
  );
};

export default Home;
