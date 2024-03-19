import React from "react";
import { Link } from "react-router-dom";

const LargeTextCard = ({ to, title, body, attributes }) => {
  return (
    <Link to={to} className="no-underline">
      <div className="lg-txt-card">
        <div className="card-body">
          <div className="flex flex-wrap gap-1">
            {attributes &&
              attributes.map((attr) => (
                <div key={attr} className="lg-txt-card-attributes">{attr}</div>
              ))}
          </div>
          <h2 className={`${title.length > 100 ? "text-sm" : "text-lg font-bold"}  p-0 m-0`}>{title}</h2>
          <p className="card2-body">{body}</p>
        </div>
      </div>
    </Link>
  );
};

export default LargeTextCard;
