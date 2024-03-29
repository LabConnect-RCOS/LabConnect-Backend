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
      <section className="text-center justify-center font-sans">
        <br/>
        <img src="LabConnect_Logo.png" alt="Logo" className="flex"></img>
        <br/>

        <p className="text-xl">
          Welcome to LabConnect!
        </p>
        <p className="text-base">
          If you are a student, go to the <Link to="/jobs" className="no-underline"><b>Jobs</b></Link> tab to view currently available research opportunities.<br/>
          If you are a professor or staff member, <Link className="no-underline"><b>Sign In</b></Link> and then go to <Link to="/createPost" className="no-underline"><b>Create</b></Link> to start posting <br/>
          opportunities or <Link to="/profile" className="no-underline"><b>Profile</b></Link> to view and edit your current posts.
        </p>
      </section>
      <section className="border-2 rounded p-2">
        <p className="text-center text-lg justify-center">
          Made by <Link to="https://new.rcos.io" className="no-underline text-red-400">RCOS</Link>
        </p>
        <div className="flex flex-row justify-between ">
          <img src="misc/LabConnect_Logo.png" alt="Logo" className="px-5 w-60 h-60"></img>
          <div className="h-60 w-40">
            <p className="text-center">
              <b>Contact Us</b>
              <p className="text-base">
                dummyemail@gmail.com<br/>other info(github/disc)
              </p>
            </p>
          </div>
          <div className="h-60 w-40 text-base">
            <b>Student Pages</b>
            <p>
              <Link to="/jobs" className="no-underline text-neutral-600 hover:text-neutral-950">Jobs</Link><br/>
              <Link to="/staff" className="no-underline text-neutral-600 hover:text-neutral-950">Staff</Link><br/>
              <Link to="/" className="no-underline text-neutral-600 hover:text-neutral-950">Sign In</Link><br/>
            </p>
          </div>
          <div className="h-60 w-60 text-base">
            <b>Staff Pages</b>
            <p>
              <Link to="/profile" className="no-underline text-neutral-600 hover:text-neutral-950">Profile</Link><br/>
              <Link to="/createPost" className="no-underline text-neutral-600 hover:text-neutral-950">Create</Link><br/>
              <Link to="/jobs" className="no-underline text-neutral-600 hover:text-neutral-950">Jobs</Link><br/>
              <Link to="/" className="no-underline text-neutral-600 hover:text-neutral-950">Sign In</Link><br/>
            </p>
          </div>
        </div>
      </section>
    </section>
  );
};

export default Home;
