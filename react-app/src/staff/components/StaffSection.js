import React from "react";
import { Link } from "react-router-dom";
import AvatarCard from "../../shared/components/UIElements/AvatarCard";

const StaffSection = ({ title, staff }) => {
  return (
    <div>
      <h4 className="font-bold py-3">{title && title}</h4>
      <div className="px-2 grid grid-cols-4" style={{ rowGap: "1.5rem" }}>
        {staff &&
          staff.map((employee) => {
            console.log(employee);
            return (
              <Link
                className="w-fit no-underline"
                key={employee.id}
                to={`/staff/${employee.id}`}
              >
                <AvatarCard name={employee.name} img={employee.image} />
              </Link>
            );
          })}
      </div>
    </div>
  );
};

export default StaffSection;
