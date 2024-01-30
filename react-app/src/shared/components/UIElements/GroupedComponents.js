import React from "react";

const GroupedComponents = ({ children, gap }) => {
  return <div className={`flex gap-${gap}`}>{children}</div>;
};

export default GroupedComponents;
