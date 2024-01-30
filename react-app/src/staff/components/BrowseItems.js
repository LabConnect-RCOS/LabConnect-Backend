import React from "react";
import LargeImageCard from "./LargeImageCard";

const BrowseItems = ({to, items}) => {
  return (
    <div className="grid grid-cols-3" style={{rowGap:'3rem'}}>
      {items.map((item) => {
        return (
          <LargeImageCard
            key={item.id}
            to={`/center/${item.title}`}
            title={item.title}
            image={item.image}
          />
        );
      })}
    </div>
  );
};

export default BrowseItems;
