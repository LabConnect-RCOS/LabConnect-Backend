import React from "react";
/*
pages = {
  pages: [Saved, Search]
  active: "Saved"
}

usePageNavigation([Saved, Search, Bookmarks], active)

=> switchPage(string)
    activePage

*/

const PageNavigation = ({ title, pages, switchPage }) => {
  const activeLink = "active-link";
  const normalLink = "normal-link hover:border-b-2 hover:text-black";

  return (
    <div className="flex gap-5" style={{ alignItems: "center" }}>
      <h1 className="text-2xl font-bold">{title}</h1>

      <nav
        className="pagenav"
        style={{ alignItems: "center" }}
      >
        {pages.pages.map((page) => {
          return (
            <button
              key={page}
              onClick={() => {
                switchPage(page);
              }}
              className={page === pages.activePage ? activeLink : normalLink}
            >
              {page}
            </button>
          );
        })}
      </nav>
    </div>
  );
};

export default PageNavigation;
