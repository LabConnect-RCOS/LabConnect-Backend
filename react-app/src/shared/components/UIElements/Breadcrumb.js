import React from "react";
import { Link } from "react-router-dom";

const LINK_TREE = [
  {
    link: "/staff",
    title: "Staff",
  },
  {
    link: "/center/CBIS",
    title: "Staff",
  },
];

const Breadcrumb = ({ tree }) => {
  return (
    <div className="text-sm breadcrumbs">
      <ul>
        {tree.map((item) => {
          return (
            <li>
              <Link to={item.link}>{item.title}</Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Breadcrumb;
