import React from "react";
import { Link } from "react-router-dom";
import AvatarCard from "../../shared/components/UIElements/AvatarCard";

const StaffSection = ({ title, staff }) => {
  return (
    <div>
      <h4 className="staff">{title && title}</h4>
      <div className="staff-body" style={{ rowGap: "1.5rem" }}>
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
