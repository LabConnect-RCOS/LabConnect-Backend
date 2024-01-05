import React, { Children } from "react";

const SmallTextButton = ({children}) => {
  return <button className="p-2 rounded-3xl border hover:text-blue-700 hover:border-blue-700">{children}</button>;
};

export default SmallTextButton;
