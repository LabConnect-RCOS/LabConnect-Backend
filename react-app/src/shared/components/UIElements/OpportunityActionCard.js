import React from "react";
import { Link } from "react-router-dom";

const OpportunityActionCard = ({ to, title, body }) => {
  
  if (title.length > 100) {title = title.slice(0, 150) + " ..."}
  
  return (
    <Link to={to} className="no-underline">
      <div className="min-h-48 max-h-48 hover:shadow-md duration-300 card card-compact w-64 p-1 bg-base-100">
        <div className="card-body">
          <h2
            className={`${
              title.length > 100 ? "text-sm" : "text-lg font-bold"
            }  p-0 m-0`}
          >
            {title}
          </h2>
          <p className="text-sm font-light p-0 m-0">{body}</p>
          <div className="card-actions justify-start">
            
              <button className="btn-sm btn btn-primary">Edit</button>
              <button className="btn-sm btn btn-primary">Deactivate</button>
              <button className="btn-sm btn btn-primary">Delete</button>
            
          </div>
        </div>
      </div>
    </Link>
  );
};

export default OpportunityActionCard;
