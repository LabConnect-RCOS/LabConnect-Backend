import React from "react";
import AvatarCard from "../../shared/components/UIElements/AvatarCard";
import StaffSection from "./StaffSection";

const DUMMY_SECTION = {
  "Artificial Intelligence": [
    {
      id: "p1",
      name: "Peter Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
    {
      id: "p2",
      name: "Peter Not Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
  ],
  "Cybersecurity": [
    {
      id: "p3",
      name: "Peter Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
    {
      id: "p4",
      name: "Peter Not Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
    {
      id: "p43t4",
      name: "Peter Not Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
  ],
  "Artificial Intelligence": [
    {
      id: "p5",
      name: "Peter Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
    {
      id: "p6",
      name: "Peter Not Johnson",
      image: "https://www.bu.edu/com/files/2015/08/Katz-James-3.jpg",
    },
  ],
};

const CenterStaff = () => {
  return (
    <div>
      {Object.keys(DUMMY_SECTION).map((key) => {
        return (
          <StaffSection key={key} title={key} staff={DUMMY_SECTION[key]} />
        );
      })}
    </div>
  );
};

export default CenterStaff;
