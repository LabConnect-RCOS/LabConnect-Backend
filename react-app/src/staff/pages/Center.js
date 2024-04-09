import React from "react";
import { useParams } from "react-router";
import Breadcrumb from "../../shared/components/UIElements/Breadcrumb";
import CenterHero from "../components/CenterHero";
import CenterStaff from "../components/CenterStaff";

const Center = ({ linkTree }) => {
  const { centerName } = useParams();
  return (
    <section className="center container-xl">
      <Breadcrumb
        tree={[
          {
            link: "/staff",
            title: "Staff",
          },
          {
            link: `/center/${centerName}`,
            title: centerName,
          },
        ]}
      />
      <CenterHero />
      <CenterStaff />
    </section>
  );
};

export default Center;
