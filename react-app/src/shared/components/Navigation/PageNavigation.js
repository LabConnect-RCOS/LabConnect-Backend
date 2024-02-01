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
  const activeLink = "text-black py-3 border-b-2 border-black text-lg";
  const normalLink =
    "text-gray-600 py-3 text-lg hover:border-b-2 border-black hover:text-black";

  return (
    <div className="flex gap-5" style={{ alignItems: "center" }}>
      <h1 className="text-2xl font-bold">{title}</h1>

      <nav
        className="text-base flex gap-4 justify-items-center font-semibold"
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
