import React from "react";
import { Link } from "react-router-dom";

const LargeImageCard = ({ to, image, title }) => {
  return (
    <Link to={to} className="no-underline">
      <div className="card card-compact w-96 bg-base-100 hover:shadow-lg transition duration-175">
        <figure>
          <img src={image} alt={title} />
        </figure>
        <div className="card-body">
          <h2 className="card-title">{title}</h2>
        </div>
      </div>
    </Link>
  );
};

export default LargeImageCard;
