import React from "react";
import { Link } from "react-router-dom";

const LargeTextCard = ({ to, title, body, attributes }) => {
  return (
    <Link to={to} className="no-underline">
      <div className="min-h-48 max-h-48 hover:shadow-md duration-300 card card-compact w-56 p-1 bg-base-100">
        <div className="card-body">
          <div className="flex flex-wrap gap-1">
            {attributes &&
              attributes.map((attr) => (
                <div key={attr} className="overflow-visible w-fit badge badge-primary">{attr}</div>
              ))}
          </div>
          <h2 className={`${title.length > 100 ? "text-sm" : "text-lg font-bold"}  p-0 m-0`}>{title}</h2>
          <p className="text-sm font-light p-0 m-0">{body}</p>
        </div>
      </div>
    </Link>
  );
};

export default LargeTextCard;
