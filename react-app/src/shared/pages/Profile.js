import React, { useEffect } from "react";
import { useState } from "react";
import ProfileAvatar from "../components/UIElements/ProfileAvatar";
import ProfileDescription from "../../staff/components/ProfileDescription";
import ProfileOpportunities from "../components/Profile/ProfileOpportunities";
import EditProfile from "./EditProfile";
import useGlobalContext from "../../context/global/useGlobalContext";
import StickyFooter from "../components/Navigation/StickyFooter.js"

const PROFILES = {
  d1: {
    name: "Peter Johnson",
    image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    researchCenter: "Computational Fake Center",
    department: "Computer Science",
    email: "johnp@rpi.edu",
    role: "admin",
    description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
          pharetra sit amet aliquam id diam maecenas ultricies mi. Montes
          nascetur ridiculus mus mauris vitae ultricies leo. Porttitor massa
          id neque aliquam. Malesuada bibendum arcu vitae elementum. Nulla
          aliquet porrsus mattis molestie aiaculis at erat pellentesque. 
          At risus viverra adipiscing at.
          Tincidunt tortor aliquam nulla facilisi cras fermentum odio eu
          feugiat. Eget fUt eu sem integer vitae justo
          eget magna fermentum. Lobortis feugiat vivamus at augue eget arcu
          dictum. Et tortor at risus viverra adipiscing at in tellus.
          Suspendisse sed nisi lacus sed viverra tellus. Potenti nullam ac
          tortor vitae. Massa id neque aliquam vestibulum. Ornare arcu odio ut
          sem nulla pharetra. Quam id leo in vitae turpis massa. Interdum
          velit euismod in pellentesque massa placerat duis ultricies lacus.
          Maecenas sed enim ut sem viverra aliquet eget sit amet. Amet
          venenatis urna cursus eget nunc scelerisque viverra mauris. Interdum
          varius sit amet mattis. Aliquet nec ullamcorper sit amet risus
          nullam. Aliquam faucibus purus in massa tempor nec feugiat. Vitae
          turpis massa sed elementum tempus. Feugiat in ante metus dictum at
          tempor. Malesuada nunc vel risus commodo viverra maecenas accumsan.
          Integer vitae justo.`,
  },
};

const ProfilePage = () => {
  const [editMode, setEditMode] = useState(false);
  const [profileFound, setProfileFound] = useState(false);
  const [profile, setProfile] = useState(null);

  const state = useGlobalContext();
  const { loggedIn } = state;

  const changeEditMode = () => {
    setEditMode(!editMode);
  };

  const { id } = state;

  useEffect(() => {
    if (id) {
      const tempProfile = PROFILES[id];

      if (tempProfile) {
        setProfile(tempProfile);
        setProfileFound(true);
      }
    }
  }, []);

  var editButton = (
    <button className="btn btn-primary my-3" onClick={changeEditMode}>
      {editMode ? "Cancel Changes" : "Edit Profile"}
    </button>
  );

  const profilePage = (
    <section>
      <div className="flex gap-5">
        <ProfileAvatar
          name={profile ? profile.name : ""}
          image={profile ? profile.image : ""}
        />
        <ProfileDescription
          name={profile ? profile.name : ""}
          researchCenter={profile ? profile.researchCenter : ""}
          department={profile ? profile.department : ""}
          description={profile ? profile.description : ""}
        />
      </div>
      <ProfileOpportunities id={id} />
    </section>
  );

  return (
    <section>
      <section>
        {!loggedIn ? (
          "Please log in to view your profile"
        ) : profileFound ? (
          <>
            {loggedIn && editButton}
            {loggedIn && editMode && <EditProfile />}
            {loggedIn && !editMode && profilePage}
          </>
        ) : (
          "Profile not found"
        )}
      </section>
      <br/><br/><br/><br/><br/><br/><br/>
      <StickyFooter />
    </section>
  );
};

export default ProfilePage;
