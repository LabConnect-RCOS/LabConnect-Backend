import React from "react";
import { CiSearch } from "react-icons/ci";

const SearchBar = () => {
  return (
    <form className="searchbar">
      <input type="text" className="" />
      <CiSearch className="text-lg" />
    </form>
  );
};

export default SearchBar;
