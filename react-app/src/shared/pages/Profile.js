import React from "react";
import { useState } from "react";
import ProfileAvatar from "../components/UIElements/ProfileAvatar";
import ProfileDescription from "../../staff/components/ProfileDescription";
import ProfileOpportunities from "../components/Profile/ProfileOpportunities";
import EditProfile from "./EditProfile";

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

  const changeEditMode = () => {
    setEditMode(!editMode);
  };

  if (!PROFILES.d1) {
    return "Profile Doesn't Exist";
  }

  const { name, image, researchCenter, department, description } = PROFILES.d1;
  
  var editButton = (
    <button className="btn btn-primary my-3" onClick={changeEditMode}>
      {editMode ? "Cancel Changes" : "Edit Profile"}
    </button>
  );

  var profile = (
    <section className="">
      <div className="flex gap-5">
        <ProfileAvatar name={name} image={image} />
        <ProfileDescription
          name={name}
          researchCenter={researchCenter}
          department={department}
          description={description}
        />
      </div>
      <ProfileOpportunities id="d1" />
    </section>
  );

  return (
    <div>
      {editButton}
      {editMode ? <EditProfile {...PROFILES.d1} id={"d1"} /> : profile}
    </div>
  );
};

export default ProfilePage;
