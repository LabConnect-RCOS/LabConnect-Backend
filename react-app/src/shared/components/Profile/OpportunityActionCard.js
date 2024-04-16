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
    <div className="opportunitycard hover:shadow-md card">
      <div className="card-body">
        <h2
          className={`${
            title.length > 100 ? "text-sm" : "text-lg font-bold"
          }  p-0 m-0`}
        >
          {title}
        </h2>
        <p className="card2-body">{body}</p>
        <div className="card-actions justify-start">
          
          
          {/* Edit button */}
          <Link to={editPath}>
            <button className="btn-sm btn btn-primary">Edit</button>
          </Link>


          {/* Deactivate Button */}
          <button
            className={buttonClass}
            onClick={() => {
              changeActiveStatus(id, activeStatus);
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
