import React from "react";

const JobPost = ({ title, professor, id, location, season, year, onClick, active }) => {
  return (
    <div className="p-2  min-h-36 flex gap-3 py-2">
      <div className={`${active && "border-l-2 border-l-purple-600"}`} />
      <div onClick={()=>{onClick(id)}} className="shadow-sm border-b border-b-gray-300 hover:bg-gray-100 p-1 rounded hover:cursor-pointer">
        <h4 className="font-black">{title}</h4>
        <div className="">
          <h5 className="text-sm">{professor}</h5>
          <h5 className="text-sm">
            {location} · {season} {year}
          </h5>
        </div>
      </div>
      
    </div>
  );
};

export default JobPost;
