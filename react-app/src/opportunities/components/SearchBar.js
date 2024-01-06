import React from "react";
import { CiSearch } from "react-icons/ci";

const SearchBar = () => {
  return (
    <form className="flex p-2 px-3 border rounded-3xl align-items-center">
      <input type="text" className="" />
      <CiSearch className="text-lg" />
    </form>
  );
};

export default SearchBar;
