import React from "react";
import ProfileAvatar from "../../shared/components/UIElements/ProfileAvatar";
import ProfileDescription from "../components/ProfileDescription";
import ProfileOpportunities from "../components/ProfileOpportunities";
import { useParams } from "react-router";

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

  if (!DUMMY_STAFF_PROFILES[staffId]) {
    return "Profile Doesn't Exist";
  }

  const { name, image, researchCenter, department, description } =
    DUMMY_STAFF_PROFILES[staffId];

  return (
    <section className="mt-5">
      <div className="flex gap-5">
        <ProfileAvatar name={name} image={image} />
        <ProfileDescription
          name={name}
          researchCenter={researchCenter}
          department={department}
          description={description}
        />
      </div>
      <ProfileOpportunities id={staffId} />
    </section>
  );
};

export default Profile;
