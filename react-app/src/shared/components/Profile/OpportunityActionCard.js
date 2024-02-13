import React from "react";
import { Link } from "react-router-dom";

const OpportunityActionCard = ({
  editPath,
  title,
  body,
  id,
  activeStatus,
  changeActiveStatus,
  deleteOpp,
}) => {
  if (title.length > 100) {
    title = title.slice(0, 150) + " ...";
  }

  const color = activeStatus ? "btn-primary" : "btn-secondary";

  const buttonClass = `btn-sm btn ${color}`;

  return (
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
          
          
          {/* Edit button */}
          <Link to={editPath}>
            <button className="btn-sm btn btn-primary">Edit</button>
          </Link>


          {/* Deactivate Button */}
          <button
            className={buttonClass}
            onClick={() => {
              changeActiveStatus(id);
            }}
          >
            {activeStatus ? "Deactivate" : "Activate"}
          </button>

          {/* Delete Button */}
          <button
            className={"btn-sm btn btn-primary"}
            onClick={() => {
              deleteOpp(id);
            }}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default OpportunityActionCard;
