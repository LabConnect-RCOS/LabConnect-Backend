import React from "react";
import Avatar from "../../shared/components/UIElements/Avatar";

const JobHeader = ({title, img, author, department}) => {
  return (
    <section className="flex flex-col gap-3">
      <h2 className="font-bold text-5xl">
        {title}
      </h2>
      <Avatar img={img} name={author} role={department} />
    </section>
  );
};

export default JobHeader;
