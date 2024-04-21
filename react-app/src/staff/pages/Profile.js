import React from "react";
import ProfileAvatar from "../../shared/components/UIElements/ProfileAvatar";
import ProfileDescription from "../components/ProfileDescription";
import ProfileOpportunities from "../components/ProfileOpportunities";
import { useParams } from "react-router";
import { useState } from "react";
import { useEffect } from "react";

const DUMMY_STAFF_PROFILES = {
  d1: {
    name: "Peter Johnson",
    image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    researchCenter: "Computational Fake Center",
    department: "Computer Science",
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

const Profile = () => {
  const { staffId } = useParams();
  var [profile, setProfile] = useState(false);

  // if (!DUMMY_STAFF_PROFILES[staffId]) {
  //   return "Profile Doesn't Exist";
  // }

  // const { name, image, researchCenter, department, description } =
  //   DUMMY_STAFF_PROFILES[staffId];

  const checkProfile = (data) => {
    return data.name && data.image && data.department && data.description;
  };

  const fetchProfile = async () => {
    const response = await fetch(
      `http://localhost:8000/getProfessorProfile/${staffId}`,
    );

    if (!response.ok) {
      setProfile("not found");
    } else {
      const data = await response.json();
      if (checkProfile(data)) {
        setProfile(data);
      } else {
        setProfile("not found");
        console.log(data);
      }
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  var profileComponents = (
    <section className="mt-5">
      <div className="flex gap-5">
        <ProfileAvatar name={profile.name} image={profile.image} />
        <ProfileDescription
          // name={profile.name}
          // researchCenter={profile.researchCenter}
          // department={department}
          // description={description}
          {...profile}
        />
      </div>
      <ProfileOpportunities id={staffId} />
    </section>
  );

  return (
    <>
      {!profile && "Loading..."}
      {typeof profile == "object" && profileComponents}
      {profile == "not found" && "Profile not found"}
    </>
  );
};

export default Profile;
